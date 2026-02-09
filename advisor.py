import google.generativeai as genai
import main as gia_vang_tool  # Gọi file main.py của bạn
import news_reader as tin_tuc_tool # Gọi file đọc báo
import os

# --- CẤU HÌNH ---
# ⚠️ THAY API KEY CỦA BẠN VÀO ĐÂY
MY_API_KEY = "AIzaSyDqj-Zm6aBp5mY6kcYAE6CiAvDTx5bhNAM" 

genai.configure(api_key=MY_API_KEY)

def xin_loi_khuyen():
    print("🤖 Đang khởi động AI Cố vấn...")

    # 1. Lấy dữ liệu giá vàng (Từ file main.py)
    df_gia = gia_vang_tool.lay_gia_vang_chuan_xac()
    if df_gia is None:
        print("❌ Không lấy được giá vàng. Dừng tư vấn.")
        return

    gia_mua = df_gia.iloc[0]['Gia_Mua']
    gia_ban = df_gia.iloc[0]['Gia_Ban']
    chenh_lech = gia_ban - gia_mua

    # 2. Lấy tin tức nóng (Từ file news_reader.py)
    # (Nếu bạn chưa tạo file news_reader, hãy tạo nó hoặc tạm thời để chuỗi rỗng)
    try:
        noi_dung_tin = tin_tuc_tool.doc_tin_tuc()
    except:
        noi_dung_tin = "Không có tin tức cụ thể."

    # 3. Soạn câu hỏi gửi cho AI (Prompt Engineering)
    cau_hoi = f"""
    Bạn là một chuyên gia phân tích tài chính đầu tư vàng lão luyện (Gold Advisor).
    Dựa trên dữ liệu thực tế sau đây, hãy đưa ra lời khuyên cho nhà đầu tư cá nhân tại Việt Nam.

    --- DỮ LIỆU THỊ TRƯỜNG ---
    1. Giá Vàng SJC hôm nay:
       - Mua vào: {gia_mua:,} VNĐ/lượng
       - Bán ra: {gia_ban:,} VNĐ/lượng
       - Chênh lệch mua-bán (Spread): {chenh_lech:,} VNĐ (Spread càng cao càng rủi ro lướt sóng).
    
    2. Tin tức kinh tế/chính trị mới nhất:
    {noi_dung_tin}

    --- YÊU CẦU ---
    Hãy phân tích ngắn gọn (dưới 10 dòng) và đưa ra kết luận:
    - XU HƯỚNG: (Tăng / Giảm / Đi ngang)
    - LỜI KHUYÊN: (Nên Mua ngay / Nên Bán chốt lời / Nên Quan sát)
    - GIẢI THÍCH: Tại sao? (Dựa trên tin tức và chênh lệch giá).
    """

    print("🚀 Đang gửi dữ liệu cho Google Gemini phân tích...")
    
    # 4. Gọi Google Gemini
    model = genai.GenerativeModel('gemini-2.5-flash') # Dùng bản Flash cho nhanh và free
    response = model.generate_content(cau_hoi)

    # 5. In kết quả
    print("\n" + "="*40)
    print("💎 KẾT QUẢ TƯ VẤN TỪ AI 💎")
    print("="*40)
    print(response.text)
    print("="*40)

if __name__ == "__main__":
    xin_loi_khuyen()