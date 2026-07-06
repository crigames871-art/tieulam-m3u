from playwright.sync_api import sync_playwright
import json

def run():
    with sync_playwright() as p:
        # Khởi chạy trình duyệt ẩn danh (Headless Chromium)
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        
        # Truy cập trang web
        print("Đang truy cập trang web...")
        page.goto("https://sv1.tieulamwc1.com/", wait_until="networkidle")
        
        # Đợi một chút để Cloudflare xử lý (nếu có)
        page.wait_for_timeout(5000)
        
        # Thử lấy dữ liệu từ API thông qua trình duyệt
        # Chúng ta dùng page.evaluate để gọi API từ trong ngữ cảnh của trình duyệt
        data = page.evaluate("""
            async () => {
                const response = await fetch('https://api.tlap17062026.com/matches/graph', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({
                        "limit": 9, "page": 1, "order_asc": "start_date",
                        "queries": [{"field": "is_top", "type": "equal", "value": true}, {"field": "blv", "type": "not_equal", "value": null}]
                    })
                });
                return await response.json();
            }
        """)
        
        browser.close()
        return data

try:
    data = run()
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

except Exception as e:
    with open('bongda.m3u', 'w', encoding='utf-8') as f:
        f.write(f"#EXTM3U\n#EXTINF:-1, Loi: {str(e)[:50]}\nhttp://error.com")
    print(f"Lỗi: {e}")
