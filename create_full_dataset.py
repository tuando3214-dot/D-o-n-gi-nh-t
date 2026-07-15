import pandas as pd
import numpy as np
import os

print("🚀 Đang khởi tạo bộ dữ liệu bất động sản chi tiết theo tiêu chuẩn đánh giá Việt Nam...")

np.random.seed(42)
n_samples = 500

# 1. THÔNG TIN CƠ BẢN & LOẠI HÌNH BẤT ĐỘNG SẢN
property_types = [
    'Căn hộ chung cư', 'Chung cư mini', 'Nhà riêng', 'Biệt thự', 
    'Nhà mặt phố', 'Nhà phố thương mại (Shophouse)', 'Trang trại', 
    'Khu nghỉ dưỡng', 'Kho', 'Xưởng'
]
chosen_types = np.random.choice(property_types, n_samples)

# 2. DIỆN TÍCH & KÍCH THƯỚC CHI TIẾT (m)
area = np.random.randint(30, 300, n_samples)
frontage = np.round(np.random.uniform(3.0, 15.0, n_samples), 1)  # Mặt tiền (m)
road_width = np.round(np.random.uniform(2.0, 20.0, n_samples), 1) # Đường vào (m)

# 3. CẤU TRÚC PHÒNG & TẦNG
bedrooms = np.random.randint(1, 6, n_samples)
bathrooms = np.random.randint(1, 5, n_samples)
toilets = bathrooms  # Số nhà vệ sinh tương đương số phòng tắm
stories = np.random.randint(1, 6, n_samples)

# 4. HƯỚNG NHÀ & HƯỚNG BAN CÔNG
directions = ['Đông', 'Tây', 'Nam', 'Bắc', 'Đông Bắc', 'Tây Bắc', 'Đông Nam', 'Tây Nam']
house_direction = np.random.choice(directions, n_samples)
balcony_direction = np.random.choice(directions, n_samples)

# 5. ĐÁNH GIÁ CHẤT LƯỢNG & PHÁP LÝ & CHỦ SỞ HỮU
legal_status = np.random.choice(['Sổ đỏ/Sổ hồng', 'Đang chờ sổ', 'Hợp đồng mua bán', 'Giấy tờ viết tay'], n_samples, p=[0.75, 0.15, 0.07, 0.03])
building_quality = np.random.choice(['Mới xây', 'Còn mới (80-90%)', 'Trung bình', 'Cần sửa chữa'], n_samples, p=[0.3, 0.4, 0.2, 0.1])
previous_owners = np.random.randint(1, 4, n_samples) # Số đời chủ trước đó

# 6. VỊ TRÍ & NỘI THẤT
locations = ['Quận Cầu Giấy, Hà Nội', 'Quận Nam Từ Liêm, Hà Nội', 'Quận Đống Đa, Hà Nội', 'Quận 1, TP.HCM', 'Quận 7, TP.HCM', 'Thành phố Thủ Đức, TP.HCM', 'TP. Bắc Ninh']
location = np.random.choice(locations, n_samples)
furniture = np.random.choice(['Không nội thất', 'Nội thất cơ bản', 'Nội thất đầy đủ / Cao cấp'], n_samples, p=[0.2, 0.5, 0.3])

# 7. LỊCH SỬ GIÁ (VND)
# Giá hiện tại (những năm gần đây)
base_m2_price = np.random.uniform(40_000_000, 120_000_000, n_samples)
current_price = np.round((area * base_m2_price) + (stories * 200_000_000), -6)

# Giá cách đây 5-10 năm (xung quanh khoảng 50% - 65% giá hiện tại)
price_5_10_years_ago = np.round(current_price * np.random.uniform(0.48, 0.65, n_samples), -6)

# 8. TIÊU ĐỀ, MÔ TẢ & THÔNG TIN LIÊN HỆ
contacts_phone = [f"09{np.random.randint(10000000, 99999999)}" for _ in range(n_samples)]
contacts_email = [f"chubatdongsan{i}@gmail.com" for i in range(1, n_samples + 1)]

titles = [f"Bán {t} diện tích {a}m2 chính chủ, vị trí đẹp tại {l}" for t, a, l in zip(chosen_types, area, location)]
descriptions = [
    f"Cần bán gấp {t}, diện tích {a}m2, mặt tiền {f}m, đường vào rộng {r}m. Nhà hướng {hd}, ban công {bd}. Pháp lý: {lg}, chất lượng {bq}. Đầy đủ tiện ích xung quanh."
    for t, a, f, r, hd, bd, lg, bq in zip(chosen_types, area, frontage, road_width, house_direction, balcony_direction, legal_status, building_quality)
]

# TẠO DATAFRAME TỔNG HỢP
df = pd.DataFrame({
    # Thông tin chung
    'title': titles,
    'description': descriptions,
    'property_type': chosen_types,
    'location': location,
    
    # Mức giá
    'price_current': current_price,                  # Giá những năm gần đây (VND)
    'price_5_10_years_ago': price_5_10_years_ago,    # Giá cách đây 5-10 năm (VND)
    
    # Đánh giá hiện trạng & Pháp lý
    'legal_status': legal_status,                     # Pháp lý
    'building_quality': building_quality,             # Chất lượng nhà
    'previous_owners': previous_owners,               # Chủ sở hữu trước đó
    'furniture': furniture,                           # Nội thất
    
    # Đồ họa & Kích thước chi tiết
    'area': area,                                     # Diện tích (m2)
    'frontage': frontage,                             # Mặt tiền (m)
    'road_width': road_width,                         # Đường vào (m)
    'bedrooms': bedrooms,                             # Số phòng ngủ
    'bathrooms': bathrooms,                           # Số phòng tắm
    'toilets': toilets,                               # Số nhà vệ sinh
    'stories': stories,                               # Số tầng
    'house_direction': house_direction,               # Hướng nhà
    'balcony_direction': balcony_direction,           # Hướng ban công
    
    # Thông tin liên hệ
    'phone': contacts_phone,
    'email': contacts_email
})

# LƯU RA FILE CSV
os.makedirs("dataset", exist_ok=True)
csv_path = "dataset/housing.csv"
df.to_csv(csv_path, index=False, encoding='utf-8-sig')

print(f"✅ THÀNH CÔNG: Đã xuất file '{csv_path}' chứa {len(df)} bản ghi bđs chi tiết đầy đủ 22 trường thông tin!")