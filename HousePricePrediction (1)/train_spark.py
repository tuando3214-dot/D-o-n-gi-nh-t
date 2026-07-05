import findspark
findspark.init()

import os
import matplotlib.pyplot as plt
import seaborn as sns
from pyspark.sql import SparkSession
from pyspark.ml.feature import VectorAssembler, StandardScaler
from pyspark.ml.regression import LinearRegression
from pyspark.ml.evaluation import RegressionEvaluator

print("=== ⚡ TIẾN TRÌNH HUẤN LUYỆN SPARK (BẬT CỬA SỔ ĐỒ THỊ) ===")

# 1. Khởi tạo một Spark Session
spark = SparkSession.builder \
    .appName("HousePricePredictionSpark") \
    .master("local[*]") \
    .getOrCreate()

spark.sparkContext.setLogLevel("ERROR")

csv_path = "dataset/housing.csv"
if not os.path.exists(csv_path):
    print(f"❌ LỖI: Không tìm thấy file dữ liệu tại {csv_path}")
    spark.stop()
    exit()

# 2. Đọc dữ liệu vào Spark DataFrame
print("-> Đang nạp dữ liệu vào Spark DataFrame...")
df = spark.read.csv(csv_path, header=True, inferSchema=True).dropna()

# 3. Gom các cột tính năng thành một Vector (Bắt buộc trong Spark ML)
feature_cols = ['area', 'bedrooms', 'bathrooms', 'stories', 'parking']
assembler = VectorAssembler(inputCols=feature_cols, outputCol="raw_features")
df_assembled = assembler.transform(df)

# 4. Chuẩn hóa dữ liệu (Scaling)
scaler = StandardScaler(inputCol="raw_features", outputCol="features", withStd=True, withMean=True)
scaler_model = scaler.fit(df_assembled)
df_scaled = scaler_model.transform(df_assembled)

# 5. Chia tập dữ liệu (80% Train, 20% Test)
train_df, test_df = df_scaled.randomSplit([0.8, 0.2], seed=42)

# 6. Huấn luyện mô hình bằng Spark ML
print("-> Đang huấn luyện mô hình bằng Spark ML...")
lr = LinearRegression(featuresCol="features", labelCol="price")
lr_model = lr.fit(train_df)

# 7. Đánh giá mô hình trên tập Test
predictions = lr_model.transform(test_df)

evaluator_r2 = RegressionEvaluator(predictionCol="prediction", labelCol="price", metricName="r2")
r2 = evaluator_r2.evaluate(predictions)

print("\n📊 KẾT QUẢ ĐÁNH GIÁ TỪ APACHE SPARK:")
print(f"--> ĐỘ CHÍNH XÁC R2: {r2 * 100:.2f}%")

# 8. Lưu mô hình Spark vào thư mục
model_dir = "model/spark_model"
lr_model.write().overwrite().save(model_dir)
print(f"✅ Đã lưu mô hình Spark vào thư mục '{model_dir}'")

# ============================================================
# 9. TIẾN TRÌNH VẼ BIỂU ĐỒ TRÒN & BẬT CỬA SỔ POP-UP (FIGURE 1)
# ============================================================
print("\n-> Đang khởi chạy và hiển thị cửa sổ biểu đồ...")
# Chuyển đổi dữ liệu Spark sang Pandas để lấy thông tin vẽ biểu đồ tròn
pdf = df.toPandas()

# Đếm số lượng nhà theo từng số lượng phòng ngủ (Bedrooms) để làm biểu đồ tròn
bedroom_counts = pdf['bedrooms'].value_counts()
labels = [f"{num} Phòng ngủ" for num in bedroom_counts.index]

# Cấu hình màu sắc pastel dịu mắt giống như hình mẫu bạn gửi
colors = ['#79b3f4', '#f19b9b', '#f7d070', '#9bf19b', '#cc9bf1']

# Khởi tạo khung vẽ
plt.figure(figsize=(7, 6))

# Vẽ biểu đồ tròn thể hiện tỷ lệ % cơ cấu phòng ngủ trong tập dữ liệu nhà
plt.pie(bedroom_counts, labels=labels, autopct='%1.1f%%', startangle=90, colors=colors[:len(labels)])
plt.title("Bieu do ty le Co cau Phong ngu tong the", fontsize=14, pad=20)

# LỆNH QUAN TRỌNG: Bật cửa sổ tương tác Figure 1 lên màn hình CMD giống y hệt mẫu
plt.show() 

# Đóng Spark Session an toàn sau khi bạn tắt cửa sổ biểu đồ
spark.stop()
print("\n==================================================\n")