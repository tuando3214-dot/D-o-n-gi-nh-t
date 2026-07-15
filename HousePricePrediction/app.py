import findspark
findspark.init()

import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os
from pyspark.sql import SparkSession
from pyspark.ml import PipelineModel

# CẤU HÌNH TRANG WEB
st.set_page_config(page_title="Dự Đoán Giá Nhà & Trực Quan Hóa", layout="wide")

@st.cache_resource
def get_spark_session():
    spark = SparkSession.builder \
        .appName("StreamlitSparkBackend") \
        .master("local[*]") \
        .getOrCreate()
    spark.sparkContext.setLogLevel("ERROR")
    return spark

spark = get_spark_session()

@st.cache_resource
def load_spark_model():
    model_path = "model/spark_model"
    if os.path.exists(model_path):
        return PipelineModel.load(model_path)
    return None

lr_model = load_spark_model()

# Đọc file CSV thực tế
csv_path = "dataset/housing.csv"
df_csv = pd.read_csv(csv_path) if os.path.exists(csv_path) else pd.DataFrame()

# Hàm lấy danh sách duy nhất từ CSV cho Dropdown
def get_options(col_name, default_list):
    if not df_csv.empty and col_name in df_csv.columns:
        return list(df_csv[col_name].dropna().unique())
    return default_list

# Khởi tạo session state lưu trữ kết quả dự đoán gần nhất
if 'last_predicted_price' not in st.session_state:
    st.session_state.last_predicted_price = None
if 'last_input_area' not in st.session_state:
    st.session_state.last_input_area = 100

# SIDEBAR
with st.sidebar:
    st.header("🔗 Thông Tin Dự Án")
    st.info("Dự án nghiên cứu Học máy nhằm dự đoán giá trị bất động sản dựa trên tập dữ liệu thực tế.")
    st.markdown("👉 📁 [Xem Mã Nguồn Trên GitHub](https://github.com/bibek376/Housing_Price_Prediction/tree/master)")
    st.markdown("---")
    st.caption("Sản phẩm hoàn thiện 100% © 2026")

st.title("🏠 Ứng Dụng Dự Đoán Giá Nhà & Trực Quan Hóa Dữ Liệu")
tab1, tab2 = st.tabs(["🎯 Dự Đoán Giá Nhà", "📊 Biểu Đồ Phân Tích Dữ Liệu"])

# ==================== TAB 1: DỰ ĐOÁN GIÁ NHÀ ====================
with tab1:
    st.subheader("📄 Nhập đầy đủ thông số căn nhà cần định giá:")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("##### 📐 Quy mô & Kích thước")
        area = st.number_input("Diện tích căn nhà (m²):", min_value=10, max_value=1000, value=100, step=5)
        frontage = st.number_input("Mặt tiền (m):", min_value=1.0, max_value=30.0, value=6.0, step=0.5)
        road_width = st.number_input("Đường vào (m):", min_value=1.0, max_value=30.0, value=8.0, step=0.5)
        stories = st.slider("Số tầng:", min_value=1, max_value=10, value=3)
        bedrooms = st.slider("Số phòng ngủ:", min_value=1, max_value=10, value=4)
        bathrooms = st.slider("Số phòng tắm:", min_value=1, max_value=8, value=2)
        toilets = st.slider("Số nhà vệ sinh:", min_value=1, max_value=8, value=3)
        previous_owners = st.slider("Số đời chủ trước:", min_value=0, max_value=5, value=1)

    with col2:
        st.markdown("##### 📍 Vị trí & Đặc tính BĐS")
        property_type = st.selectbox("Loại bất động sản:", get_options('property_type', ['Nhà riêng', 'Nhà mặt phố', 'Biệt thự']))
        location = st.selectbox("Vị trí / Khu vực:", get_options('location', ['Hà Nội', 'TP. Hồ Chí Minh', 'Đà Nẵng']))
        legal_status = st.selectbox("Tình trạng pháp lý:", get_options('legal_status', ['Sổ đỏ/Sổ hồng', 'Đang chờ sổ', 'Giấy tờ viết tay']))
        building_quality = st.selectbox("Chất lượng xây dựng:", get_options('building_quality', ['Mới xây', 'Còn tốt', 'Cần sửa chữa']))

    with col3:
        st.markdown("##### 🧭 Phong thủy & Nội thất")
        furniture = st.selectbox("Tình trạng nội thất:", get_options('furniture', ['Đầy đủ', 'Cơ bản', 'Không nội thất']))
        house_direction = st.selectbox("Hướng nhà:", get_options('house_direction', ['Đông', 'Tây', 'Nam', 'Bắc', 'Đông Nam', 'Đông Bắc', 'Tây Nam', 'Tây Bắc']))
        balcony_direction = st.selectbox("Hướng ban công:", get_options('balcony_direction', ['Đông', 'Tây', 'Nam', 'Bắc', 'Đông Nam', 'Đông Bắc', 'Tây Nam', 'Tây Bắc']))

    st.markdown("---")
    
    if st.button("💵 DỰ ĐOÁN GIÁ CĂN NHÀ", type="primary"):
        if lr_model is None:
            st.error("❌ Không tìm thấy mô hình Spark! Vui lòng chạy file `train_spark.py` trước.")
        else:
            input_data = [(
                float(area), float(frontage), float(road_width), float(bedrooms),
                float(bathrooms), float(toilets), float(stories), float(previous_owners),
                str(property_type), str(location), str(legal_status),
                str(building_quality), str(furniture), str(house_direction), str(balcony_direction)
            )]
            cols = [
                'area', 'frontage', 'road_width', 'bedrooms', 'bathrooms', 'toilets', 'stories', 'previous_owners',
                'property_type', 'location', 'legal_status', 'building_quality', 'furniture', 'house_direction', 'balcony_direction'
            ]
            input_spark_df = spark.createDataFrame(input_data, schema=cols)
            
            prediction_df = lr_model.transform(input_spark_df)
            predicted_price = float(prediction_df.select("prediction").collect()[0][0])
            
            # Lưu dữ liệu vừa dự đoán vào State
            st.session_state.last_predicted_price = predicted_price
            st.session_state.last_input_area = area
            
            st.success(f"### 🎉 Kết quả định giá thực tế từ Apache Spark: **{predicted_price:,.0f} VNĐ**")

# ==================== TAB 2: BIỂU ĐỒ PHÂN TÍCH ====================
with tab2:
    st.subheader("📊 Xu hướng biến động và vị trí căn nhà bạn vừa định giá")
    
    if not df_csv.empty and 'price_current' in df_csv.columns:
        
        # Thông báo nếu người dùng đã bấm dự đoán
        if st.session_state.last_predicted_price is not None:
            st.info(f"📍 **Căn nhà mới chọn:** Diện tích: **{st.session_state.last_input_area} m²** | Giá dự đoán: **{st.session_state.last_predicted_price:,.0f} VNĐ** (Điểm đỏ trên biểu đồ)")
        
        col_chart1, col_chart2 = st.columns(2)
        
        with col_chart1:
            st.markdown("**1. Vị trí căn nhà mới định giá trên biểu đồ Diện tích vs Giá:**")
            fig1, ax1 = plt.subplots(figsize=(7, 4.5))
            sns.scatterplot(data=df_csv, x='area', y='price_current', ax=ax1, color='#4c72b0', alpha=0.5, label='Dữ liệu lịch sử')
            
            # Tự động vẽ thêm điểm đỏ mới nếu đã bấm dự đoán
            if st.session_state.last_predicted_price is not None:
                ax1.scatter(
                    st.session_state.last_input_area, 
                    st.session_state.last_predicted_price, 
                    color='red', s=180, zorder=5, label='Nhà bạn vừa chọn'
                )
            
            ax1.set_title("Vị trí căn nhà mới chọn trên tập dữ liệu", fontsize=12)
            ax1.set_xlabel("Diện tích (m²)")
            ax1.set_ylabel("Giá nhà (VNĐ)")
            ax1.legend()
            st.pyplot(fig1)
            
        with col_chart2:
            st.markdown("**2. Vị trí Giá căn nhà vừa định giá trên Phân phối mật độ:**")
            fig2, ax2 = plt.subplots(figsize=(7, 4.5))
            sns.kdeplot(data=df_csv['price_current'], ax=ax2, color='#55a868', fill=True, alpha=0.4, label='Phân bổ giá chung')
            
            # Tự động vẽ đường nét đứt đỏ mới chỉ giá vừa tính
            if st.session_state.last_predicted_price is not None:
                ax2.axvline(
                    st.session_state.last_predicted_price, 
                    color='red', linestyle='--', linewidth=2.5, label='Giá dự đoán nhà bạn'
                )
            
            ax2.set_title("Mật độ phân bổ các mức giá", fontsize=12)
            ax2.set_xlabel("Giá nhà (VNĐ)")
            ax2.set_ylabel("Mật độ")
            ax2.legend()
            st.pyplot(fig2)
            
        st.markdown("---")
        
        # HÀNG 2: MỨC TĂNG TRƯỞNG TRUNG BÌNH
        if 'price_5_10_years_ago' in df_csv.columns:
            st.markdown("**3. Mức giá trung bình So sánh giữa Giá hiện tại và Giá 5 - 10 năm trước:**")
            avg_current = df_csv['price_current'].mean()
            avg_past = df_csv['price_5_10_years_ago'].mean()
            growth_rate = ((avg_current - avg_past) / avg_past) * 100 if avg_past > 0 else 0
            
            col_metric1, col_metric2, col_metric3 = st.columns(3)
            col_metric1.metric("Giá trung bình 5-10 năm trước", f"{avg_past:,.0f} VNĐ")
            col_metric2.metric("Giá trung bình hiện tại", f"{avg_current:,.0f} VNĐ")
            col_metric3.metric("Tỉ lệ tăng trưởng trung bình", f"+{growth_rate:.1f}%")

            fig3, ax3 = plt.subplots(figsize=(10, 3.8))
            df_compare = pd.DataFrame({
                'Giai đoạn': ['Giá 5-10 năm trước', 'Giá hiện tại'],
                'Giá trung bình (VNĐ)': [avg_past, avg_current]
            })
            sns.barplot(data=df_compare, x='Giai đoạn', y='Giá trung bình (VNĐ)', palette=['#79706e', '#d62728'], ax=ax3)
            ax3.set_title("So sánh mức giá BĐS trung bình qua các mốc thời gian", fontsize=12)
            st.pyplot(fig3)

            st.markdown("---")
        
        # HÀNG 3: MA TRẬN TƯƠNG QUAN
        st.markdown("**4. Ma trận tương quan giữa các yếu tố (Correlation Matrix):**")
        numeric_cols_plot = ['price_current', 'price_5_10_years_ago', 'area', 'frontage', 'road_width', 'bedrooms', 'bathrooms', 'toilets', 'stories', 'previous_owners']
        existing_cols = [c for c in numeric_cols_plot if c in df_csv.columns]
        
        fig4, ax4 = plt.subplots(figsize=(12, 4.5))
        sns.heatmap(df_csv[existing_cols].corr(), annot=True, cmap='coolwarm', fmt=".2f", ax=ax4, vmin=-1, vmax=1)
        st.pyplot(fig4)
        
    else:
        st.warning("⚠️ Không tìm thấy file 'dataset/housing.csv' để trích xuất biểu đồ.")