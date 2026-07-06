from curl_cffi import requests

api_url = "https://api.tlap17062026.com/matches/graph"

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36',
    'Accept': 'application/json, text/plain, */*',
    'Content-Type': 'application/json',
    'Origin': 'https://sv1.tieulamwc1.com',
    'Referer': 'https://sv1.tieulamwc1.com/'
}

payload = {
    "limit": 9,
    "page": 1,
    "order_asc": "start_date",
    "queries": [
        {"field": "is_top", "type": "equal", "value": True},
        {"field": "blv", "type": "not_equal", "value": None}
    ]
}

try:
    # Thử gọi trực tiếp, nếu lỗi sẽ in ra nội dung để chẩn đoán
    response = requests.post(api_url, headers=headers, json=payload, impersonate="chrome120", timeout=15)
    
    if response.status_code == 200:
        data = response.json()
        # ... (Phần xử lý m3u giữ nguyên như cũ) ...
        print("Kết nối thành công!")
    else:
        # GHI LẠI LỖI VÀO FILE M3U ĐỂ BẠN ĐỌC
        error_content = f"#EXTM3U\n#EXTINF:-1, LOI: {response.status_code}\n"
        error_content += f"#EXTINF:-1, NOI DUNG TRANG WEB TRA VE:\n"
        error_content += f"#EXTINF:-1, {response.text[:200]}" # Chỉ lấy 200 ký tự đầu
        with open('bongda.m3u', 'w', encoding='utf-8') as f:
            f.write(error_content)
        print(f"Lỗi {response.status_code}. Đã ghi lỗi vào file bongda.m3u để kiểm tra.")

except Exception as e:
    with open('bongda.m3u', 'w', encoding='utf-8') as f:
        f.write(f"#EXTM3U\n#EXTINF:-1, Loi exception: {str(e)[:50]}")
