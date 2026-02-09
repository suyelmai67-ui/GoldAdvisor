import google.generativeai as genai

# ⚠️ DÁN KEY CỦA BẠN VÀO ĐÂY
MY_API_KEY = "DÁN_KEY_CỦA_BẠN_VÀO_ĐÂY" 

genai.configure(api_key=MY_API_KEY)

print("🔍 Đang kiểm tra danh sách Model...")
try:
    found = False
    for m in genai.list_models():
        # Chỉ tìm những model biết chat (generateContent)
        if 'generateContent' in m.supported_generation_methods:
            print(f"- ✅ Có thể dùng: {m.name}")
            found = True
            
    if not found:
        print("❌ Key hợp lệ nhưng không tìm thấy Model nào. Có thể do mạng hoặc lỗi tài khoản.")
        
except Exception as e:
    print(f"❌ LỖI KEY: {e}")
    print("👉 Hãy kiểm tra lại xem đã copy đúng hết ký tự của Key chưa?")