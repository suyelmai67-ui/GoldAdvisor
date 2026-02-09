import feedparser

# Link RSS của VnExpress (Nguồn tin chính thống, cập nhật nhanh)
RSS_URL = "https://vnexpress.net/rss/kinh-doanh.rss"

def doc_tin_tuc():
    print("📰 Đang tải tin tức tài chính từ VnExpress...")
    
    # Tải dữ liệu RSS
    feed = feedparser.parse(RSS_URL)
    
    tin_hot = []
    dem = 0
    
    # Duyệt qua các bài báo (Lấy tối đa 10 bài mới nhất)
    for entry in feed.entries:
        if dem >= 5: # Chỉ lấy 5 tin quan trọng nhất để không bị quá tải
            break
            
        tieu_de = entry.title
        tom_tat = entry.summary
        
        # Chỉ lấy tin liên quan đến tiền bạc, vàng, thế giới
        tu_khoa = ['vàng', 'gold', 'usd', 'lãi suất', 'chiến tranh', 'lạm phát', 'fed', 'tỷ giá', 'xăng', 'dầu']
        
        # Kiểm tra: Nếu tiêu đề hoặc tóm tắt có chứa từ khóa thì mới lấy
        noi_dung_kiem_tra = (tieu_de + " " + tom_tat).lower()
        
        if any(tu in noi_dung_kiem_tra for tu in tu_khoa):
            print(f"-> Tìm thấy tin: {tieu_de}")
            tin_hot.append(f"- Tiêu đề: {tieu_de}\n  Tóm tắt: {tom_tat}")
            dem += 1
            
    if len(tin_hot) == 0:
        return "Không có tin tức nổi bật về tài chính hôm nay."
        
    return "\n".join(tin_hot)

# --- CHẠY THỬ ---
if __name__ == "__main__":
    ket_qua = doc_tin_tuc()
    print("\n--- NỘI DUNG SẼ GỬI CHO AI ---")
    print(ket_qua)