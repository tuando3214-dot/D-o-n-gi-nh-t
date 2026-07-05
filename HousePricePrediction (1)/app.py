import streamlit as st
import pandas as pd
import joblib
import os
import matplotlib.pyplot as plt
import seaborn as sns

# Cấu hình trang web
st.set_page_config(page_title="Dự đoán giá nhà", page_icon="🏠", layout="wide")

# --- PHẦN THANH BÊN (SIDEBAR) CHỨA THÔNG TIN MÃ NGUỒN ---
st.sidebar.title("🔗 Thông Tin Dự Án")
st.sidebar.info("Dự án nghiên cứu Học máy nhằm dự đoán giá trị bất động sản dựa trên tập dữ liệu thực tế.")

# Đã chèn chính xác link nguồn Github của bạn vào đây
github_url = "https://github.com/bibek376/Housing_Price_Prediction/tree/master"
st.sidebar.markdown(f"👉 [📂 Xem Mã Nguồn Trên GitHub]({github_url})")

st.sidebar.divider()
st.sidebar.caption("Sản phẩm hoàn thiện 100% © 2026")


# --- PHẦN GIAO DIỆN CHÍNH ---
st.title("🏠 Ứng Dụng Dự Đoán Giá Nhà & Trực Quan Hóa Dữ Liệu")

# Kiểm tra file mô hình và file dữ liệu
model_path = "model/house_model.pkl"
csv_path = "dataset/housing.csv"

if not os.path.exists(model_path) or not os.path.exists(csv_path):
    st.error("❌ Thiếu file hệ thống! Vui lòng đảm bảo đã có file 'dataset/housing.csv' và đã chạy 'train.py'.")
else:
    # Tải dữ liệu và mô hình lên
    df = pd.read_csv(csv_path).dropna()
    artifacts = joblib.load(model_path)
    model = artifacts['model']
    scaler = artifacts['scaler']

    # Chia giao diện làm 2 tab: Dự đoán & Phân tích biểu đồ
    tab1, tab2 = st.tabs(["🎯 Dự Đoán Giá Nhà", "📊 Biểu Đồ Phân Tích Dữ Liệu"])

    # ---------------- TAB 1: DỰ ĐOÁN GIÁ ----------------
    with tab1:
        st.subheader("📝 Nhập thông số căn nhà cần định giá:")
        
        col1, col2 = st.columns(2)
        with col1:
            area = st.number_input("Diện tích căn nhà (sqft):", min_value=100, max_value=20000, value=4000, step=50)
            bedrooms = st.slider("Số phòng ngủ:", min_value=1, max_value=8, value=3)
            bathrooms = st.slider("Số phòng vệ sinh:", min_value=1, max_value=5, value=2)
        with col2:
            stories = st.slider("Số tầng:", min_value=1, max_value=4, value=2)
            parking = st.slider("Chỗ đỗ xe ô tô:", min_value=0, max_value=4, value=1)
            
        st.write("")
        if st.button("💵 DỰ ĐOÁN GIÁ CĂN NHÀ", type="primary"):
            input_data = pd.DataFrame([{
                'area': area, 'bedrooms': bedrooms, 'bathrooms': bathrooms, 'stories': stories, 'parking': parking
            }])
            input_scaled = scaler.transform(input_data)
            prediction = model.predict(input_scaled)
            st.success(f"### 💰 Giá trị ước tính của căn nhà: **{prediction[0]:,.2f} USD**")

    # ---------------- TAB 2: BIỂU ĐỒ ----------------
    with tab2:
        st.subheader("📊 Xu hướng phân bổ dữ liệu thực tế từ file CSV")
        
        col_chart1, col_chart2 = st.columns(2)
        
        with col_chart1:
            st.write("**1. Mối quan hệ giữa Diện tích (Area) và Giá nhà (Price):**")
            fig1, ax1 = plt.subplots(figsize=(6, 4))
            sns.scatterplot(data=df, x='area', y='price', alpha=0.6, ax=ax1, color='#1f77b4')
            ax1.set_title("Diện tích tăng thì Giá nhà tăng theo")
            ax1.set_xlabel("Diện tích (sqft)")
            ax1.set_ylabel("Giá nhà (USD)")
            st.pyplot(fig1)

        with col_chart2:
            st.write("**2. Biểu đồ phân phối Giá nhà trong tập dữ liệu:**")
            fig2, ax2 = plt.subplots(figsize=(6, 4))
            sns.histplot(df['price'], kde=True, ax=ax2, color='#2ca02c')
            ax2.set_title("Mật độ phân bổ của các mức giá")
            ax2.set_xlabel("Giá nhà (USD)")
            ax2.set_ylabel("Số lượng căn")
            st.pyplot(fig2)
            
        st.divider()
        st.write("**3. Ma trận tương quan giữa các yếu tố (Correlation Matrix):**")
        fig3, ax3 = plt.subplots(figsize=(8, 4))
        sns.heatmap(df[['price', 'area', 'bedrooms', 'bathrooms', 'stories', 'parking']].corr(), annot=True, cmap='coolwarm', fmt=".2f", ax=ax3)
        st.pyplot(fig3)