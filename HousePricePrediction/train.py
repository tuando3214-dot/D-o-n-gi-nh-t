import os
import pandas as pd
import joblib
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import r2_score, mean_absolute_error

print("=== 🚀 TIẾN TRÌNH HUẤN LUYỆN MÔ HÌNH NÂNG CẤP (TRAIN) ===")

# 1. Đọc dữ liệu
csv_path = "dataset/housing.csv"
df = pd.read_csv(csv_path).dropna()

feature_cols = ['area', 'bedrooms', 'bathrooms', 'stories', 'parking']
target_col = 'price'

X = df[feature_cols]
y = df[target_col]

# Chia tập dữ liệu (80% Train, 20% Test)
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# 2. Chuẩn hóa dữ liệu (Scaling)
scaler = StandardScaler()
X_train_scaled = scaler.fit_transform(X_train)
X_test_scaled = scaler.transform(X_test)

# 3. Huấn luyện bằng Random Forest
print("-> Đang huấn luyện bằng thuật toán Random Forest Regressor...")
model = RandomForestRegressor(n_estimators=100, random_state=42)
model.fit(X_train_scaled, y_train)

# 4. Đánh giá mô hình nâng cấp
y_pred = model.predict(X_test_scaled)
r2 = r2_score(y_test, y_pred)
mae = mean_absolute_error(y_test, y_pred)

print(f"\n📊 KẾT QUẢ SAU KHI TỐI ƯU:")
print(f"--> ĐỘ CHÍNH XÁC R2 MỚI: {r2 * 100:.2f}%")
print(f"--> Sai số tuyệt đối trung bình (MAE): {mae:,.2f} USD")

# 5. Lưu cả Mô hình và Bộ chuẩn hóa dữ liệu vào chung một file pkl
model_dir = "model"
if not os.path.exists(model_dir):
    os.makedirs(model_dir)

artifacts = {
    'model': model,
    'scaler': scaler,
    'features': feature_cols
}

joblib.dump(artifacts, os.path.join(model_dir, "house_model.pkl"))
print("\n✅ THÀNH CÔNG: Đã lưu mô hình tối ưu vào 'model/house_model.pkl'")
print("========================================================\n")