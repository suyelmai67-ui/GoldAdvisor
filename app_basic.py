import streamlit as st
import pandas as pd
import google.generativeai as genai
import main as gia_vang_tool
import news_reader as tin_tuc_tool
import os

# --- CẤU HÌNH TRANG WEB ---
st.set_page_config(
    page_title="Gold Advisor AI - Trợ Lý Vàng 2026",
    page_icon="💰",
    layout="wide"
)

# ==========================================
# ⚠️ DÁN API KEY CỦA BẠN VÀO ĐÂY (Trong ngoặc kép)
RAW_KEY = "AIzaSyDqj-Zm6aBp5mY6kcYAE6CiAvDTx5bhNAM"
# ==========================================

# Cấu hình AI (Tự động làm sạch Key)
MY_API_KEY = RAW_KEY.strip()
genai.configure(api_key=MY_API_KEY)

# --- GIAO DIỆN ---
st.title("🌟 AI CỐ VẤN ĐẦU TƯ VÀNG (Gold Advisor)")
st.markdown("### Hệ thống theo dõi giá vàng SJC & Phân tích thị trường tự động")

# Chia màn hình làm 2 cột: Cột 1 (Biểu đồ) rộng gấp đôi Cột 2 (AI)
col1, col2 = st.columns([2, 1])

# --- CỘT 1: BIỂU ĐỒ GIÁ ---
with col1:
    st.subheader("📊 Biểu đồ biến động giá vàng SJC")
    
    # Đọc dữ liệu từ file CSV
    if os.path.isfile('gold_history.csv'):
        try:
            df = pd.read_csv('gold_history.csv')
            
            # Vẽ biểu đồ đường (Line Chart)
            # Trục tung là Giá Mua và Giá Bán
            st.line_chart(df.set_index('Gio')[['Gia_Mua', 'Gia_Ban']])
            
            # Hiện bảng số liệu chi tiết bên dưới
            st.write("Dữ liệu chi tiết 5 lần cập nhật gần nhất:")
            st.dataframe(df.tail(5), use_container_width=True)
            
        except Exception as e:
            st.error(f"Lỗi đọc file dữ liệu: {e}")
    else:
        st.warning("⚠️ Chưa có dữ liệu lịch sử! Hãy bấm nút phân tích bên cạnh để hệ thống bắt đầu thu thập.")

# --- CỘT 2: AI TƯ VẤN ---
with col2:
    st.subheader("🤖 AI Phân Tích")
    st.markdown("Bấm nút dưới đây để AI đọc báo và đưa ra lời khuyên.")
    
    # Nút bấm hành động
    if st.button("🚀 PHÂN TÍCH THỊ TRƯỜNG NGAY", type="primary"):
        with st.spinner("Đang lấy giá vàng & Đọc báo..."):
            try:
                # 1. Lấy giá vàng mới nhất (Real-time)
                df_new = gia_vang_tool.lay_gia_vang_chuan_xac()
                
                # Nếu lấy được giá thì lưu vào file luôn để vẽ biểu đồ
                if df_new is not None:
                    gia_vang_tool.luu_file(df_new)
                    
                    # Lấy số liệu để gửi cho AI
                    gia_mua = df_new.iloc[0]['Gia_Mua']
                    gia_ban = df_new.iloc[0]['Gia_Ban']
                    chenh_lech = gia_ban - gia_mua
                else:
                    st.error("❌ Không lấy được giá vàng! Kiểm tra lại kết nối mạng.")
                    st.stop() # Dừng lại, không chạy tiếp

                # 2. Đọc tin tức kinh tế
                tin_tuc = tin_tuc_tool.doc_tin_tuc()
                
                # 3. Soạn câu hỏi gửi cho AI (Prompt)
                prompt = f"""
                Bạn là chuyên gia tài chính năm 2026. Dữ liệu thực tế vừa cập nhật:
                - Giá Vàng SJC: Mua {gia_mua:,} VNĐ - Bán {gia_ban:,} VNĐ.
                - Chênh lệch Mua-Bán: {chenh_lech:,} VNĐ.
                - Tin tức thị trường nóng hổi: 
                {tin_tuc}
                
                Hãy phân tích ngắn gọn và đưa ra lời khuyên cho nhà đầu tư cá nhân:
                1. Xu hướng sắp tới (Tăng/Giảm)?
                2. Hành động: Nên Mua, Bán hay Giữ?
                3. Giải thích lý do (dựa trên tin tức và giá)?
                """
                
                # 4. Gọi Google Gemini (Dùng model mới nhất bạn vừa tìm được)
                model = genai.GenerativeModel('gemini-2.5-flash')
                response = model.generate_content(prompt)
                
                # 5. Hiện kết quả ra màn hình
                st.success("✅ Phân tích hoàn tất!")
                
                # Dùng st.info để đóng khung lời khuyên cho đẹp
                st.info(response.text)
                
                # Nút làm mới trang (để cập nhật biểu đồ bên trái)
                if st.button("🔄 Cập nhật biểu đồ"):
                    st.rerun()
                
            except Exception as e:
                st.error(f"Lỗi AI: {e}")

    else:
        st.write("👈 Bấm nút để bắt đầu.")