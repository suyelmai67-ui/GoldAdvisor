import google.generativeai as genai

# ==========================================
# DÁN KEY CỦA BẠN VÀO GIỮA 2 DẤU NGOẶC KÉP
# (Code sẽ tự động cắt bỏ dấu cách thừa nếu bạn lỡ tay)
RAW_KEY = "AIzaSyDqj-Zm6aBp5mY6kcYAE6CiAvDTx5bhNAM"
# ==========================================

MY_API_KEY = RAW_KEY.strip()
genai.configure(api_key=MY_API_KEY)

print(f"🔑 Đang kiểm tra với Key: {MY_API_KEY[:5]}... (Đã ẩn đuôi)")
print("📡 Đang kết nối tới Google để lấy danh sách Model...")

try:
    found = False
    print("\n--- DANH SÁCH MODEL KHẢ DỤNG ---")
    for m in genai.list_models():
        # Chỉ liệt kê các model biết chat (generateContent)
        if 'generateContent' in m.supported_generation_methods:
            print(f"✅ {m.name}")
            found = True
            
    if not found:
        print("❌ Kết nối được nhưng không thấy Model nào. (Lạ nhỉ?)")
    else:
        print("-" * 30)
        print("👉 HÃY COPY MỘT CÁI TÊN Ở TRÊN (Ví dụ: models/gemini-pro)")
        print("   VÀ DÁN VÀO FILE advisor.py NHÉ!")

except Exception as e:
    print(f"❌ LỖI: {e}")