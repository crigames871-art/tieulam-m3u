import requests

api_url = "https://api.tlap17062026.com/matches/graph"

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
    'Referer': 'https://sv1.tieulamwc1.com/',
    'Origin': 'https://sv1.tieulamwc1.com',
    'Content-Type': 'application/json'
}

try:
    # Gửi yêu cầu
    response = requests.post(api_url, headers=headers, json={}, timeout=15)
    
    # Kiểm tra nếu bị Cloudflare chặn (Phản hồi không phải 200)
    if response.status_code != 200:
        with open('bongda.m3u', 'w', encoding='utf-8') as f:
            f.write(f"#EXTM3U\n#EXTINF:-1, Bị chặn mã lỗi: {response.status_code}\nhttp://error.com")
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
        m3u_content += "#EXTINF:-1, API không trả về trận nào hoặc trống\nhttp://error.com"

    with open('bongda.m3u', 'w', encoding='utf-8') as f:
        f.write(m3u_content)
    print(f"Xong! Tìm thấy {count} trận.")

except Exception as e:
    with open('bongda.m3u', 'w', encoding='utf-8') as f:
        f.write(f"#EXTM3U\n#EXTINF:-1, Lỗi Code: {str(e)[:50]}\nhttp://error.com")
    print(f"Lỗi: {e}")
