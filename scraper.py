from playwright.sync_api import sync_playwright
import json

def run():
    with sync_playwright() as p:
        # Cấu hình trình duyệt giống người dùng thật
        browser = p.chromium.launch(headless=True)
        context = browser.new_context(
            user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36"
        )
        page = context.new_page()
        
        # Biến lưu trữ dữ liệu
        api_data = None

        # Thiết lập "cái bẫy" để bắt lấy dữ liệu khi trang web tải xong
        def handle_response(response):
            nonlocal api_data
            if "api.tlap17062026.com/matches/graph" in response.url:
                try:
                    api_data = response.json()
                except:
                    pass

        page.on("response", handle_response)

        # Truy cập trang web
        print("Đang truy cập...")
        page.goto("https://sv1.tieulamwc1.com/", wait_until="networkidle")
        
        # Đợi thêm 5 giây để chắc chắn các yêu cầu API đã chạy xong
        page.wait_for_timeout(5000)
        
        browser.close()
        return api_data

try:
    data = run()
    
    if data and 'data' in data:
        m3u_content = "#EXTM3U\n"
        count = 0
        for match in data.get('data', []):
            title = match.get('title')
            m3u8_link = match.get('source_live')
            if m3u8_link:
                m3u_content += f"#EXTINF:-1, {title}\n{m3u8_link}\n"
                count += 1
                
        with open('bongda.m3u', 'w', encoding='utf-8') as f:
            f.write(m3u_content)
        print(f"Thành công! Lấy được {count} trận.")
    else:
        print("Không bắt được dữ liệu API.")
        with open('bongda.m3u', 'w', encoding='utf-8') as f:
            f.write("#EXTM3U\n#EXTINF:-1, Khong lay duoc du lieu API\nhttp://error.com")

except Exception as e:
    with open('bongda.m3u', 'w', encoding='utf-8') as f:
        f.write(f"#EXTM3U\n#EXTINF:-1, Loi: {str(e)[:50]}\nhttp://error.com")
