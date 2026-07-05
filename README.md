# 🏠 Dự Án Dự Đoán Giá Nhà (House Price Prediction Hub)

Dự án nghiên cứu và triển khai Học máy (Machine Learning) toàn diện nhằm dự đoán giá trị bất động sản dựa trên các thuộc tính thực tế từ dữ liệu (`housing.csv`): diện tích, số phòng ngủ, phòng tắm, số tầng và chỗ đậu xe.

Điểm nổi bật của dự án là việc kết hợp đồng thời giữa mô hình học máy truyền thống (**Scikit-Learn Random Forest**) và framework xử lý dữ liệu lớn (**Apache Spark MLlib**), đi kèm giao diện web trực quan sinh động bằng **Streamlit**.

---

## 📊 Tổng Quan Tập Dữ Liệu (`housing.csv`)
Tập dữ liệu chứa thông tin thực tế của các căn nhà với các thuộc tính định lượng và định danh:
* `price`: Giá nhà (Biến mục tiêu cần dự đoán)
* `area`: Diện tích căn nhà (sqft)
* `bedrooms`: Số lượng phòng ngủ
* `bathrooms`: Số lượng phòng vệ sinh
* `stories`: Số tầng của căn nhà
* `parking`: Số chỗ đỗ xe ô tô

---

## 🛠️ Cấu Trúc Mã Nguồn Dự Án
```bash
📂 Housing_Price_Prediction
├── 📂 dataset
│   └── housing.csv          # Tập dữ liệu gốc dạng CSV
├── 📂 model
│   ├── house_model.pkl      # Mô hình Scikit-Learn đã huấn luyện
│   └── spark_model/         # Thư mục lưu mô hình Apache Spark MLlib
├── app.py                   # 🌐 Giao diện Web Dashboard (Streamlit)
├── train.py                 # 🚀 Huấn luyện mô hình Scikit-Learn (Random Forest)
├── train_spark.py           # ⚡ Huấn luyện mô hình Apache Spark (Linear Regression)
├── predict.py               # 🔮 Dự đoán giá nhà nhanh từ terminal
├── README.md                # 📝 Tài liệu hướng dẫn dự án (File này)
└── shortcuts.json           # Cấu hình phím tắt tiện ích bổ sung
🚀 Tính Năng Chính & Các Tiến Trình Chạy
1. Huấn Luyện Mô Hình Scikit-Learn (train.py)
Sử dụng thuật toán Random Forest Regressor kết hợp chuẩn hóa dữ liệu StandardScaler để tối ưu độ chính xác. Tập dữ liệu được chia theo tỷ lệ 80% Train / 20% Test. Sau khi hoàn tất, mô hình sẽ tự động lưu lại thành file model/house_model.pkl.

Lệnh chạy:

Bash
python train.py
2. Huấn Luyện Dữ Liệu Lớn Với Apache Spark (train_spark.py)
Sử dụng Apache Spark MLlib với thuật toán Linear Regression giúp xử lý tính toán song song, tối ưu hiệu năng cho tập dữ liệu lớn.

Tự động gom tính năng bằng VectorAssembler và chuẩn hóa qua StandardScaler.

Xuất đánh giá mô hình bằng chỉ số R 
2
  (Độ chính xác).

Tích hợp vẽ và hiển thị biểu đồ tròn (Pie Chart) phân tích tỷ lệ số lượng phòng ngủ bằng Matplotlib & Seaborn với tone màu pastel dịu mắt.

Lệnh chạy:

Bash
python train_spark.py
3. Giao Diện Định Giá Nhà Trực Tuyến (app.py)
Ứng dụng Web hoàn chỉnh được xây dựng trên framework Streamlit chia làm 2 phân hệ (Tabs):

Tab 1: 🔮 Dự đoán giá nhà: Cho phép người dùng tùy chỉnh các thông số (Diện tích, số phòng, số tầng...) thông qua thanh trượt hoặc ô nhập liệu trực quan để nhận báo giá căn nhà ước tính theo thời gian thực.

Tab 2: 📊 Biểu đồ trực quan: Trình bày mối quan hệ tuyến tính giữa Diện tích & Giá nhà qua biểu đồ Scatter plot, đồng thời hiển thị lược đồ mật độ phân bổ mức giá (KDE Histogram).

Lệnh chạy:

Bash
streamlit run app.py
4. Thử Nghiệm Dự Đoán Nhanh (predict.py)
File kịch bản terminal giúp nạp nhanh "bộ não" mô hình house_model.pkl để đưa ra giá trị ước tính cho một căn nhà mẫu mặc định hoặc nhập tùy ý.

Lệnh chạy:

Bash
python predict.py
🛠️ Hướng Dẫn Cài Đặt Khởi Chạy Từ A - Z
Để chạy mượt mà toàn bộ dự án trên máy tính của bạn, hãy làm theo các bước hướng dẫn chi tiết dưới đây:

Bước 1: Tải mã nguồn về máy
Mở Terminal / Command Prompt và gõ lệnh:

Bash
git clone [https://github.com/bibek376/Housing_Price_Prediction.git](https://github.com/bibek376/Housing_Price_Prediction.git)
cd Housing_Price_Prediction
Bước 2: Cài đặt các thư viện phụ thuộc
Đảm bảo máy tính của bạn đã cài đặt Python (Khuyến nghị >= 3.8). Tiến hành cài đặt các gói phụ thuộc:

Bash
pip install streamlit pandas matplotlib seaborn scikit-learn joblib findspark pyspark
Lưu ý đối với Apache Spark (train_spark.py): Bạn cần cấu hình sẵn môi trường Java (JDK) và Apache Spark trên hệ điều hành máy tính để chạy được các tiến trình Big Data.

Bước 3: Huấn luyện tạo mô hình học máy
Trước khi khởi chạy giao diện web hoặc kiểm tra dự đoán, bạn cần tạo ra file mô hình bằng cách chạy tệp huấn luyện:

Bash
python train.py
Bước 4: Khởi chạy Giao diện Web Dashboard
Bật Server Streamlit để trải nghiệm ứng dụng ngay trên trình duyệt web của bạn (http://localhost:8501):

Bash
streamlit run app.py
📈 Kết Quả Đánh Giá & Hiển Thị
Thuật toán áp dụng: Random Forest Regressor (Scikit-Learn) & Linear Regression (Spark ML).

Biểu đồ tích hợp: Biểu đồ mật độ phân phối (Distribution), Biểu đồ tương quan (Scatter plot), Biểu đồ tròn cơ cấu (Pie chart).

Hiệu năng: Hệ thống dự đoán phản hồi tức thì (< 0.5s) trên giao diện Streamlit ngay sau khi người dùng tinh chỉnh tham số.

Sản phẩm hoàn thiện 100% © 2026. Phát triển nhằm mục đích nghiên cứu và tối ưu hóa ứng dụng Học máy vào thực tiễn Bất động sản.
