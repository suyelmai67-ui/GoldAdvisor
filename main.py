import requests
import pandas as pd
from datetime import datetime, timedelta
import os

# --- CẤU HÌNH ---
URL = "https://giavang.org/"
FILE_NAME = 'gold_history.csv'

def lay_gia_vang_chuan_xac():
    print(f"Dang ket noi den {URL}...")
    
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }
    
    try:
        response = requests.get(URL, headers=headers)
        danh_sach_bang = pd.read_html(response.text)
        
        if len(danh_sach_bang) == 0:
            print("❌ Không tìm thấy bảng giá!")
            return None
        
        df = danh_sach_bang[0]
        
        gia_mua = 0
        gia_ban = 0
        found = False

        print("--- Đang phân tích bảng giá SJC ---")
        
        for index, row in df.iterrows():
            row_text = str(row.values)
            
            # Tìm dòng SJC TP. Hồ Chí Minh
            if "Hồ Chí Minh" in row_text and "SJC" in row_text:
                print(f"📍 Tìm thấy dữ liệu thô: {row_text}")
                
                cac_so = []
                for cot in row:
                    # Xóa ký tự lạ để lấy số
                    text_clean = str(cot).lower().replace('đ', '').replace('.', '').replace(',', '').strip()
                    
                    if text_clean.isdigit():
                        so = int(text_clean)
                        
                        # --- SỬA LOGIC Ở ĐÂY ---
                        # Nếu web viết tắt (ví dụ 177400), ta nhân 1000 để thành 177 triệu
                        if so < 1000000: 
                            so = so * 1000
                            print(f"-> Đã quy đổi đơn vị: {so:,}")

                        # Lọc giá rác: Chỉ lấy giá > 50 triệu
                        if so > 50000000:
                            cac_so.append(so)
                
                cac_so.sort()
                if len(cac_so) >= 2:
                    gia_mua = cac_so[0]
                    gia_ban = cac_so[1]
                    found = True
                    break

        if not found or gia_mua == 0:
            print("⚠️ Không lấy được giá hợp lệ.")
            return None

        print(f"💰 GIÁ VÀNG SJC CHỐT: Mua {gia_mua:,} - Bán {gia_ban:,}")

        gio_vn = datetime.utcnow() + timedelta(hours=7)
        du_lieu = {
            'Ngay': [gio_vn.strftime("%Y-%m-%d")],
            'Gio': [gio_vn.strftime("%H:%M:%S")],
            'Loai_Vang': ['SJC_HCM'],
            'Gia_Mua': [gia_mua],
            'Gia_Ban': [gia_ban]
        }
        return pd.DataFrame(du_lieu)

    except Exception as e:
        print(f"❌ Lỗi: {e}")
        return None

def luu_file(du_lieu_moi):
    if not os.path.isfile(FILE_NAME):
        du_lieu_moi.to_csv(FILE_NAME, index=False)
    else:
        du_lieu_moi.to_csv(FILE_NAME, mode='a', header=False, index=False)
    print("📁 Đã lưu dữ liệu thành công!")

if __name__ == "__main__":
    df = lay_gia_vang_chuan_xac()
    if df is not None:
        luu_file(df)