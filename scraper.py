from curl_cffi import requests
import json
import random

api_url = "https://api.tlap17062026.com/matches/graph"

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

# Danh sách các proxy công cộng miễn phí để phân tán dải IP của GitHub
proxy_list = [
    "http://sp09b78809:scpb659ef8@gate.scrapersandbox.com:80",
    "http://185.195.155.105:1080",
    "http://51.79.51.52:8080",
    "http://167.71.218.169:8080"
]

success = False
response_data = None

# Thử chạy trực tiếp không proxy trước, nếu lỗi 403 sẽ tự động kích hoạt proxy thay thế
print("Đang thử kết nối trực tiếp...")
try:
    response = requests.post(api_url, headers=headers, json=payload, impersonate="chrome", timeout=10)
    if response.status_code == 200:
        response_data = response.json()
        success = True
    else:
        print(f"Kết nối trực tiếp thất bại với mã lỗi: {response.status_code}. Tiến hành chuyển sang Proxy...")
except Exception as e:
    print(f"Lỗi kết nối trực tiếp: {e}. Tiến hành thử nghiệm các cổng Proxy...")

# Nếu bị chặn, thử lần lượt qua danh sách proxy
if not success:
    random.shuffle(proxy_list) # Tráo ngẫu nhiên thứ tự proxy để tăng tỷ lệ sống
    for proxy in proxy_list:
        print(f"Đang thử kết nối qua mặt nạ IP: {proxy.split('@')[-1] if '@' in proxy else proxy}")
        try:
            proxies = {"http": proxy, "https": proxy}
            response = requests.post(api_url, headers=headers, json=payload, proxies=proxies, impersonate="chrome", timeout=12)
            
            if response.status_code == 200:
                response_data = response.json()
                success = True
                print("Ẩn IP thành công! Đã vượt qua tường lửa Cloudflare.")
                break
            else:
                print(f"Proxy phản hồi mã lỗi: {response.status_code}, tiếp tục đổi proxy khác...")
        except Exception as proxy_err:
            print(f"Proxy gặp sự cố kết nối, đang đổi...")

# Xử lý ghi dữ liệu ra file m3u
if success and response_data:
    m3u_content = "#EXTM3U\n"
    count = 0
    
    for match in response_data.get('data', []):
        title = match.get('title')
        m3u8_link = match.get('source_live')
        is_live = match.get('is_live', False)
        
        if m3u8_link:
            trang_thai = "[LIVE] " if is_live else "[SẮP ĐÁ] "
            m3u_content += f"#EXTINF:-1, {trang_thai}{title}\n"
            m3u_content += f"#EXTVLCOPT:http-referrer=https://sv1.tieulamwc1.com/\n"
            m3u_content += f"{m3u8_link}\n"
            count += 1
            print(f"Đã cập nhật trận đấu: {title}")
            
    if count == 0:
        m3u_content += "#EXTINF:-1, API chay tot nhung hien tai khong co tran nao live\nhttp://error.com"
        print("Vượt rào thành công nhưng hiện tại trang web chưa có luồng phát sóng.")
        
    with open('bongda.m3u', 'w', encoding='utf-8') as f:
        f.write(m3u_content)
else:
    # Nếu tất cả các phương án đều thất bại
    with open('bongda.m3u', 'w', encoding='utf-8') as f:
        f.write("#EXTM3U\n#EXTINF:-1, Tat ca cac dai IP deu bi chan 403\nhttp://error.com")
    print("Hệ thống Cloudflare quá nghiêm ngặt. Cần kiểm tra lại sau ít phút hoặc đổi proxy cao cấp hơn.")
