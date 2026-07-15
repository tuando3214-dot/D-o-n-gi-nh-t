import findspark
findspark.init()

import os
import shutil
from pyspark.sql import SparkSession
from pyspark.ml.feature import VectorAssembler, StandardScaler, StringIndexer
from pyspark.ml.regression import LinearRegression
from pyspark.ml import Pipeline

print("🚀 Bắt đầu tiến trình huấn luyện mô hình PySpark với ĐẦY ĐỦ thông tin...")

# 1. Khởi tạo Spark Session
spark = SparkSession.builder \
    .appName("HousePriceTrainerFull") \
    .master("local[*]") \
    .getOrCreate()
spark.sparkContext.setLogLevel("ERROR")

# 2. Tải dữ liệu từ CSV
csv_path = "dataset/housing.csv"
if not os.path.exists(csv_path):
    print(f"❌ Không tìm thấy file '{csv_path}'. Vui lòng kiểm tra lại đường dẫn!")
    exit()

df = spark.read.csv(csv_path, header=True, inferSchema=True)

# 3. Phân loại các cột đặc trưng
numeric_cols = ['area', 'frontage', 'road_width', 'bedrooms', 'bathrooms', 'toilets', 'stories', 'previous_owners']
categorical_cols = ['property_type', 'location', 'legal_status', 'building_quality', 'furniture', 'house_direction', 'balcony_direction']
target_col = 'price_current'

# Ép kiểu cho các cột số
for c in numeric_cols + [target_col]:
    if c in df.columns:
        df = df.withColumn(c, df[c].cast("double"))

# Mã hóa các cột dạng chữ (Categorical) sang dạng số cho Spark
indexers = [
    StringIndexer(inputCol=c, outputCol=f"{c}_indexed", handleInvalid="keep")
    for c in categorical_cols if c in df.columns
]

indexed_cat_cols = [f"{c}_indexed" for c in categorical_cols if c in df.columns]
assembler_inputs = [c for c in numeric_cols if c in df.columns] + indexed_cat_cols

# 4. Xây dựng Pipeline chuẩn hóa và huấn luyện
assembler = VectorAssembler(inputCols=assembler_inputs, outputCol="raw_features")
scaler = StandardScaler(inputCol="raw_features", outputCol="features", withStd=True, withMean=True)
lr = LinearRegression(featuresCol="features", labelCol=target_col)

pipeline = Pipeline(stages=indexers + [assembler, scaler, lr])
model = pipeline.fit(df)

# 5. Lưu mô hình Spark
model_path = "model/spark_model"
if os.path.exists(model_path):
    shutil.rmtree(model_path)

model.save(model_path)
print(f"✅ HUẤN LUYỆN THÀNH CÔNG ĐẦY ĐỦ! Mô hình đã lưu tại '{model_path}'.")