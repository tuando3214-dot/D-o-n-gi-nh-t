import time
import re
import pandas as pd
from DrissionPage import ChromiumPage

def clean_number(text):
    """Trích xuất con số từ chuỗi text"""
    if not text:
        return None
    numbers = re.findall(r'[\d\.\,]+', str(text))
    if numbers:
        num_str = numbers[0].replace('.', '').replace(',', '.')
        try:
            return float(num_str)
        except:
            return None
    return None

def parse_price(price_str):
    """Chuyển đổi các định dạng giá (Tỷ, Triệu, Triệu/m2) sang VND chuẩn"""
    if not price_str:
        return None
    price_str = price_str.lower().strip()
    
    if 'tỷ' in price_str:
        val = clean_number(price_str)
        return val * 1_000_000_000 if val else None
    elif 'triệu' in price_str and 'm²' not in price_str and 'm2' not in price_str:
        val = clean_number(price_str)
        return val * 1_000_000 if val else None
    return None

def parse_area(area_str):
    """Trích xuất diện tích m²"""
    if not area_str:
        return None
    return clean_number(area_str)

def crawl_batdongsan(max_pages=3):
    print("🚀 Bắt đầu mở trình duyệt cào dữ liệu Batdongsan.com.vn...")
    page = ChromiumPage()
    
    data_list = []
    
    for page_num in range(1, max_pages + 1):
        url = f"https://batdongsan.com.vn/nha-dat-ban/p{page_num}"
        print(f"\n📄 Đang cào trang {page_num}: {url}")
        
        page.get(url)
        time.sleep(4) # Chờ trang tải đầy đủ DOM và vượt Cloudflare
        
        # Tìm danh sách các thẻ bđs
        cards = page.eles('.js__product-link-for-product-id')
        if not cards:
            # Thu thập theo class thẻ bài chuẩn của Batdongsan
            cards = page.eles('xpath://div[contains(@class, "re__card-info")]')
            
        print(f"-> Tìm thấy {len(cards)} tin đăng bất động sản.")
        
        for card in cards:
            try:
                # Lấy Giá
                price_ele = card.ele('.re__card-config-price', timeout=1)
                price_text = price_ele.text if price_ele else ""
                price = parse_price(price_text)
                
                # Lấy Diện tích
                area_ele = card.ele('.re__card-config-area', timeout=1)
                area_text = area_ele.text if area_ele else ""
                area = parse_area(area_text)
                
                # Lấy Số phòng ngủ
                bedroom_ele = card.ele('.re__card-config-bedroom', timeout=1)
                bedrooms = clean_number(bedroom_ele.text) if bedroom_ele else 2 # Mặc định 2 nếu ẩn
                
                # Lấy Số phòng toilet / Tầng (Gán giá trị hợp lý nếu không hiển thị ở card ngoài)
                toilet_ele = card.ele('.re__card-config-toilet', timeout=1)
                bathrooms = clean_number(toilet_ele.text) if toilet_ele else 2
                
                stories = 1
                parking = 1
                
                # Chỉ lấy bản ghi có đủ thông tin Giá và Diện tích
                if price and area and price > 0 and area > 0:
                    data_list.append({
                        'price': price,
                        'area': area,
                        'bedrooms': int(bedrooms) if bedrooms else 2,
                        'bathrooms': int(bathrooms) if bathrooms else 1,
                        'stories': int(stories),
                        'parking': int(parking)
                    })
            except Exception as e:
                continue
                
    page.quit()
    
    # Lưu ra file dataset/housing.csv
    if data_list:
        df = pd.DataFrame(data_list)
        # Loại bỏ các dữ liệu ngoại lệ quá dị biệt (Outliers)
        df = df[(df['price'] > 100_000_000) & (df['area'] > 10)]
        
        import os
        os.makedirs("dataset", exist_ok=True)
        csv_path = "dataset/housing.csv"
        df.to_csv(csv_path, index=False)
        print(f"\n✅ CÀO THÀNH CÔNG: Đã lưu {len(df)} bản ghi bđs thực tế vào '{csv_path}'!")
    else:
        print("\n❌ Không lấy được dữ liệu. Hãy kiểm tra lại kết nối internet hoặc đường dẫn!")

if __name__ == "__main__":
    crawl_batdongsan(max_pages=2) # Thay đổi số trang muốn cào ở đây