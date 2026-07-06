import requests

api_url = "https://api.tlap17062026.com/matches/graph"

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
    'Referer': 'https://sv1.tieulamwc1.com/',
    'Origin': 'https://sv1.tieulamwc1.com',
    'Content-Type': 'application/json'
}

# Cấu trúc dữ liệu gửi đi lấy chính xác từ tab Payload của bạn
payload = {
    "limit": 9,
    "page": 1,
    "order_asc": "start_date",
    "queries": [
        {"field": "is_top", "type": "equal", "value": True},
        {"field": "blv", "type": "not_equal", "value": None} # None trong Python tương đương với null trong JSON
    ]
}

try:
    # Gửi yêu cầu POST kèm theo dữ liệu bộ lọc (payload)
    response = requests.post(api_url, headers=headers, json=payload, timeout=15)
    
    # Kiểm tra nếu máy chủ chặn hoặc lỗi đường truyền
    if response.status_code != 200:
        with open('bongda.m3u', 'w', encoding='utf-8') as f:
            f.write(f"#EXTM3U\n#EXTINF:-1, API bao loi HTTP: {response.status_code}\nhttp://error.com")
        print(f"Lỗi HTTP: {response.status_code}")
        exit(0)

    # Thử đọc dữ liệu JSON, nếu lỗi sẽ in ra nội dung phản hồi thực tế để dễ kiểm tra
    try:
        data = response.json()
    except Exception as json_err:
        print("Không thể giải mã JSON. Nội dung thực tế từ Server:")
        print(response.text[:500]) # In ra 500 ký tự đầu tiên để xem phản hồi là gì
        with open('bongda.m3u', 'w', encoding='utf-8') as f:
            f.write(f"#EXTM3U\n#EXTINF:-1, Server phan hoi khong phai JSON\nhttp://error.com")
        exit(0)
        
    m3u_content = "#EXTM3U\n"
    count = 0
    
    # Duyệt qua danh sách trận đấu nhận được
    for match in data.get('data', []):
        title = match.get('title')
        m3u8_link = match.get('source_live')
        is_live = match.get('is_live', False)
        
        # Nếu trận đấu có link m3u8 thì đưa vào danh sách IPTV
        if m3u8_link:
            trang_thai = "[LIVE] " if is_live else "[SẮP ĐÁ] "
            m3u_content += f"#EXTINF:-1, {trang_thai}{title}\n"
            m3u_content += f"#EXTVLCOPT:http-referrer=https://sv1.tieulamwc1.com/\n"
            m3u_content += f"{m3u8_link}\n"
            count += 1
            print(f"Đã thêm: {title}")
            
    if count == 0:
        m3u_content += "#EXTINF:-1, API hien tai khong co link m3u8 nao\nhttp://error.com"
        print("API hoạt động nhưng hiện tại không có trận nào có link luồng (.m3u8).")

    with open('bongda.m3u', 'w', encoding='utf-8') as f:
        f.write(m3u_content)
    print(f"Hoàn thành! Đã nạp thành công {count} trận đấu vào file.")

except Exception as e:
    with open('bongda.m3u', 'w', encoding='utf-8') as f:
        f.write(f"#EXTM3U\n#EXTINF:-1, Loi code: {str(e)[:50]}\nhttp://error.com")
    print(f"Lỗi hệ thống: {e}")
