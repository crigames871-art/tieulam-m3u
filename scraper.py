import requests

api_url = "https://api.tlap17062026.com/matches/graph"

# Bộ Headers tối tân giả lập y hệt trình duyệt Cốc Cốc/Chrome thật
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
    'Accept': 'application/json, text/plain, */*',
    'Accept-Language': 'vi-VN,vi;q=0.9,en-US;q=0.8,en;q=0.7',
    'Content-Type': 'application/json',
    'Origin': 'https://sv1.tieulamwc1.com',
    'Referer': 'https://sv1.tieulamwc1.com/',
    'Sec-Ch-Ua': '"Not A(Brand";v="99", "Chromium";v="120", "Google Chrome";v="120"',
    'Sec-Ch-Ua-Mobile': '?0',
    'Sec-Ch-Ua-Platform': '"Windows"',
    'Sec-Fetch-Dest': 'empty',
    'Sec-Fetch-Mode': 'cors',
    'Sec-Fetch-Site': 'cross-site',
    'Connection': 'keep-alive'
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
    # Sử dụng một Session để giữ kết nối ổn định giống trình duyệt
    session = requests.Session()
    response = session.post(api_url, headers=headers, json=payload, timeout=15)
    
    if response.status_code != 200:
        with open('bongda.m3u', 'w', encoding='utf-8') as f:
            f.write(f"#EXTM3U\n#EXTINF:-1, Cloudflare chan (HTTP {response.status_code})\nhttp://error.com")
        print(f"Lỗi HTTP: {response.status_code}")
        exit(0)

    data = response.json()
    m3u_content = "#EXTM3U\n"
    count = 0
    
    for match in data.get('data', []):
        title = match.get('title')
        m3u8_link = match.get('source_live')
        is_live = match.get('is_live', False)
        
        if m3u8_link:
            trang_thai = "[LIVE] " if is_live else "[SẮP ĐÁ] "
            m3u_content += f"#EXTINF:-1, {trang_thai}{title}\n"
            m3u_content += f"#EXTVLCOPT:http-referrer=https://sv1.tieulamwc1.com/\n"
            m3u_content += f"{m3u8_link}\n"
            count += 1
            
    if count == 0:
        m3u_content += "#EXTINF:-1, API hoat dong nhung khong co tran nao\nhttp://error.com"

    with open('bongda.m3u', 'w', encoding='utf-8') as f:
        f.write(m3u_content)
    print(f"Thành công! Tìm thấy {count} trận.")

except Exception as e:
    with open('bongda.m3u', 'w', encoding='utf-8') as f:
        f.write(f"#EXTM3U\n#EXTINF:-1, Loi Code: {str(e)[:50]}\nhttp://error.com")
    print(f"Lỗi: {e}")
