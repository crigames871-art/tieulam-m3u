from curl_cffi import requests
import json

api_url = "https://api.tlap17062026.com/matches/graph"

# Bộ headers chuẩn từ trình duyệt
headers = {
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
    # impersonate="chrome" sẽ ép curl_cffi giả lập vân tay trình duyệt Chrome để qua mặt Cloudflare
    response = requests.post(
        api_url, 
        headers=headers, 
        json=payload, 
        impersonate="chrome", 
        timeout=15
    )
    
    if response.status_code != 200:
        with open('bongda.m3u', 'w', encoding='utf-8') as f:
            f.write(f"#EXTM3U\n#EXTINF:-1, Cloudflare van chan (HTTP {response.status_code})\nhttp://error.com")
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
            print(f"Đã thêm trận: {title}")
            
    if count == 0:
        m3u_content += "#EXTINF:-1, API hoat dong nhung hien tai het tran\nhttp://error.com"
        print("Vượt Cloudflare thành công nhưng danh sách trận đấu trống.")
    else:
        print(f"Thành công vượt Cloudflare! Lấy được {count} trận.")

    with open('bongda.m3u', 'w', encoding='utf-8') as f:
        f.write(m3u_content)

except Exception as e:
    with open('bongda.m3u', 'w', encoding='utf-8') as f:
        f.write(f"#EXTM3U\n#EXTINF:-1, Loi Code: {str(e)[:50]}\nhttp://error.com")
    print(f"Lỗi hệ thống: {e}")
