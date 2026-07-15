import os
import pandas as pd
import joblib

print("=== TIẾN TRÌNH DỰ ĐOÁN GIÁ NHÀ (PREDICT) ===")

model_path = "model/house_model.pkl"
if not os.path.exists(model_path):
    print(f"❌ LỖI: Không tìm thấy file mô hình. Bạn cần chạy file 'train.py' trước!")
    exit()

model = joblib.load(model_path)
print("✅ Đã nạp bộ não mô hình thành công!")

# Tạo dữ liệu một căn nhà mới dựa trên các thông số thực tế của bạn để đoán thử
# Ví dụ căn nhà: Diện tích (area) = 4000, 3 phòng ngủ, 2 phòng vệ sinh, 2 tầng, 1 chỗ đỗ xe
new_house = pd.DataFrame([{
    'area': 4000,
    'bedrooms': 3,
    'bathrooms': 2,
    'stories': 2,
    'parking': 1
}])

print("\n-> Thông tin căn nhà mới cần định giá:")
print(new_house)

# Chạy dự đoán
predicted_price = model.predict(new_house)
print(f"\n💵 GIÁ DỰ ĐOÁN CỦA CĂN NHÀ LÀ: {predicted_price[0]:,.2f}")
print("========================================================\n")