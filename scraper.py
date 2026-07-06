import requests

# Địa chỉ API chính xác từ tab Headers của bạn
api_url = "https://api.tlap17062026.com/matches/graph"

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
    'Referer': 'https://sv1.tieulamwc1.com/',
    'Origin': 'https://sv1.tieulamwc1.com',
    'Content-Type': 'application/json'
}

try:
    # Gửi yêu cầu POST (kèm body trống json={} vì đây là phương thức POST)
    response = requests.post(api_url, headers=headers, json={}, timeout=15)
    
    # Đọc dữ liệu định dạng JSON
    data = response.json()
    
    m3u_content = "#EXTM3U\n"
    count = 0
    
    # Duyệt qua danh sách các trận đấu trả về từ API
    for match in data.get('data', []):
        title = match.get('title')
        m3u8_link = match.get('source_live')
        is_live = match.get('is_live', False)
        
        # Nếu trận đấu có link phát m3u8 thì ghi vào file
        if m3u8_link:
            trang_thai = "[LIVE] " if is_live else "[SẮP ĐÁ] "
            m3u_content += f"#EXTINF:-1, {trang_thai}{title}\n"
            m3u_content += f"#EXTVLCOPT:http-referrer=https://sv1.tieulamwc1.com/\n"
            m3u_content += f"{m3u8_link}\n"
            count += 1
            print(f"Đã thêm trận: {title}")
            
    # Ghi nội dung vào file bongda.m3u
    with open('bongda.m3u', 'w', encoding='utf-8') as f:
        f.write(m3u_content)
        
    print(f"Thành công! Đã quét được {count} trận đấu vào file m3u.")

except Exception as e:
    print(f"Lỗi khi xử lý dữ liệu từ API: {e}")
