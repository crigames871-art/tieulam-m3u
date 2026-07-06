from playwright.sync_api import sync_playwright
import json

def run():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        context = browser.new_context(
            user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36"
        )
        page = context.new_page()
        
        # 1. Truy cập trang chủ để nhận Cookie/Session
        print("Truy cập trang chủ để lấy Session...")
        page.goto("https://sv1.tieulamwc1.com/", wait_until="networkidle")
        
        # 2. Gọi trực tiếp API với Payload mà chúng ta đã thấy trong tab Network
        print("Gọi trực tiếp API...")
        api_url = "https://api.tlap17062026.com/matches/graph"
        payload = {
            "limit": 9,
            "page": 1,
            "order_asc": "start_date",
            "queries": [{"field": "is_top", "type": "equal", "value": True}, {"field": "blv", "type": "not_equal", "value": None}]
        }
        
        # Sử dụng page.request để gửi POST request, nó sẽ tự kèm theo Cookies từ trình duyệt
        response = page.request.post(api_url, json=payload)
        
        data = None
        if response.ok:
            data = response.json()
        
        browser.close()
        return data

# Phần xử lý và lưu file
try:
    result = run()
    
    if result and 'data' in result:
        m3u_content = "#EXTM3U\n"
        matches = result.get('data', [])
        count = 0
        for match in matches:
            title = match.get('title')
            m3u8_link = match.get('source_live')
            if m3u8_link:
                m3u_content += f"#EXTINF:-1, {title}\n{m3u8_link}\n"
                count += 1
        
        if count > 0:
            with open('bongda.m3u', 'w', encoding='utf-8') as f:
                f.write(m3u_content)
            print(f"Thành công! Đã lưu {count} trận.")
        else:
            print("API trả về nhưng không có dữ liệu trận đấu.")
    else:
        print("Không lấy được dữ liệu từ API.")
        print(f"Phản hồi API: {result}")

except Exception as e:
    print(f"Lỗi hệ thống: {e}")
