import streamlit as st
import pandas as pd
import google.generativeai as genai
import main as gia_vang_tool
import news_reader as tin_tuc_tool
import os
import time

# --- 1. CẤU HÌNH TRANG WEB ---
st.set_page_config(
    page_title="Gold Advisor Pro 2026",
    page_icon="💎",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# --- 2. CSS LÀM ĐẸP ---
st.markdown("""
<style>
    .main-title {
        font-size: 3rem !important;
        font-weight: 800 !important;
        color: #FFD700 !important;
        text-align: center;
        text-shadow: 2px 2px 4px #000000;
        margin-bottom: 20px;
    }
    div[data-testid="stMetricValue"] {
        font-size: 1.8rem !important;
        color: #00FF00;
    }
    .stButton > button {
        width: 100%;
        border-radius: 20px;
        font-weight: bold;
        background: linear-gradient(45deg, #FFD700, #FFA500);
        border: none;
        color: black;
        height: 50px;
    }
    .stButton > button:hover {
        box-shadow: 0px 0px 15px #FFD700;
        color: white;
    }
    .ai-box {
        background-color: #262730;
        padding: 20px;
        border-radius: 10px;
        border-left: 5px solid #FFD700;
        margin-top: 20px;
    }
</style>
""", unsafe_allow_html=True)

# --- 3. CẤU HÌNH API KEY ---
# ==========================================
# ⚠️⚠️⚠️ DÁN KEY THẬT CỦA BẠN VÀO DÒNG DƯỚI ĐÂY
# --- CẤU HÌNH API KEY AN TOÀN ---
import os
try:
    # Lấy key từ "Két sắt" (Secrets) của Streamlit
    MY_API_KEY = st.secrets["GOOGLE_API_KEY"]
except:
    # Nếu chạy trên máy tính cá nhân (không có Secrets)
    # Bạn có thể dán tạm key vào đây ĐỂ TEST, NHƯNG ĐỪNG UP LÊN GITHUB
    MY_API_KEY = "DÁN_KEY_MỚI_VÀO_ĐÂY_CHỈ_KHI_CHẠY_Ở_MÁY_NHÀ"

genai.configure(api_key=MY_API_KEY)
# ==========================================
MY_API_KEY = RAW_KEY.strip()
try:
    genai.configure(api_key=MY_API_KEY)
except:
    st.error("Lỗi API Key! Hãy kiểm tra lại key trong file app_pro.py")

# --- 4. KHỞI TẠO BỘ NHỚ (SESSION STATE) ---
# Đây là phần quan trọng để AI "nhớ" kết quả
if 'ai_result' not in st.session_state:
    st.session_state['ai_result'] = ""
if 'last_update' not in st.session_state:
    st.session_state['last_update'] = "Chưa cập nhật"

# --- 5. GIAO DIỆN CHÍNH ---
st.markdown('<p class="main-title">🌟 GOLD ADVISOR PRO 2026 🌟</p>', unsafe_allow_html=True)
st.divider()

col_left, col_right = st.columns([7, 3], gap="large")

# ======================= CỘT TRÁI: DỮ LIỆU =======================
with col_left:
    st.subheader("📊 Dữ Liệu Thị Trường")
    
    # Đọc dữ liệu
    df = None
    if os.path.isfile('gold_history.csv'):
        try:
            df = pd.read_csv('gold_history.csv')
        except:
            pass

    # Hiển thị số liệu (Metrics)
    m1, m2, m3 = st.columns(3)
    if df is not None and not df.empty:
        last_row = df.iloc[-1]
        mua = last_row['Gia_Mua']
        ban = last_row['Gia_Ban']
        spread = ban - mua
        
        m1.metric("💰 Mua Vào", f"{mua:,.0f} VNĐ")
        m2.metric("💸 Bán Ra", f"{ban:,.0f} VNĐ")
        m3.metric("↔️ Chênh Lệch", f"{spread:,.0f} VNĐ")
    else:
        m1.metric("Giá Mua", "Wait...")
        m2.metric("Giá Bán", "Wait...")
        m3.metric("Spread", "Wait...")

    # Biểu đồ
    with st.container(border=True):
        if df is not None and not df.empty:
            chart_data = df.set_index('Gio')[['Gia_Mua', 'Gia_Ban']]
            st.line_chart(chart_data, color=["#00FF00", "#FF4500"], height=350)
        else:
            st.info("Chưa có dữ liệu. Hãy bấm nút Phân Tích.")

# ======================= CỘT PHẢI: AI CỐ VẤN =======================
with col_right:
    st.subheader("🤖 AI Phân Tích")
    
    # Nút bấm
    if st.button("🚀 PHÂN TÍCH NGAY", type="primary"):
        with st.status("🤖 AI đang làm việc...", expanded=True) as status:
            try:
                # B1: Lấy giá
                st.write("📡 Đang lấy giá vàng...")
                df_new = gia_vang_tool.lay_gia_vang_chuan_xac()
                
                if df_new is not None:
                    gia_vang_tool.luu_file(df_new)
                    mua_new = df_new.iloc[0]['Gia_Mua']
                    ban_new = df_new.iloc[0]['Gia_Ban']
                    chenh_lech = ban_new - mua_new
                else:
                    st.error("Không lấy được giá!")
                    st.stop()

                # B2: Đọc báo
                st.write("📰 Đang đọc tin tức...")
                tin_tuc = tin_tuc_tool.doc_tin_tuc()

                # B3: Gọi AI
                st.write("🧠 Đang suy nghĩ...")
                prompt = f"""
                Bạn là chuyên gia tài chính 2026. Dữ liệu:
                - Giá Vàng: Mua {mua_new:,} - Bán {ban_new:,}.
                - Tin tức: {tin_tuc}
                
                Hãy đưa ra lời khuyên ngắn gọn:
                1. Xu hướng (Tăng/Giảm)?
                2. Nên Mua hay Bán?
                3. Tại sao? (Ngắn gọn)
                """
                
                model = genai.GenerativeModel('gemini-2.5-flash')
                response = model.generate_content(prompt)
                
                # B4: LƯU KẾT QUẢ VÀO BỘ NHỚ (Khắc phục lỗi mất chữ)
                st.session_state['ai_result'] = response.text
                st.session_state['last_update'] = time.strftime("%H:%M:%S")
                
                status.update(label="✅ Xong!", state="complete", expanded=False)
                time.sleep(0.5)
                st.rerun() # Làm mới để cập nhật biểu đồ

            except Exception as e:
                st.error(f"Lỗi: {e}")

    # HIỂN THỊ KẾT QUẢ TỪ BỘ NHỚ (Nằm ngoài nút bấm)
    st.write(f"🕒 Cập nhật lần cuối: {st.session_state['last_update']}")
    
    if st.session_state['ai_result']:
        st.success("Kết quả phân tích:")
        st.markdown(f'<div class="ai-box">{st.session_state["ai_result"]}</div>', unsafe_allow_html=True)
    else:
        st.info("👈 Bấm nút để xem lời khuyên.")