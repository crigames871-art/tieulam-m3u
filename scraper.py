from playwright.sync_api import sync_playwright
import json

def run():
    with sync_playwright() as p:
        # 1. Khởi chạy với chế độ tàng hình (ẩn dấu vết automation)
        browser = p.chromium.launch(
            headless=True,
            args=["--disable-blink-features=AutomationControlled", "--no-sandbox"]
        )
        
        context = browser.new_context(
            user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36"
        )
        page = context.new_page()

        # 2. Bộ bắt lỗi để xem chính xác lý do tại sao bị "Abort"
        page.on("requestfailed", lambda request: print(f"LỖI KẾT NỐI: {request.url} - Lý do: {request.failure}"))

        # 3. Truy cập trang chủ
        print("Đang truy cập trang chủ...")
        page.goto("https://sv1.tieulamwc1.com/", wait_until="domcontentloaded")
        page.wait_for_timeout(3000)

        # 4. Gửi yêu cầu với đầy đủ Headers để không bị chặn
        print("Đang gửi yêu cầu tới API...")
        api_url = "https://api.tlap17062026.com/matches/graph"
        payload = {
            "limit": 9,
            "page": 1,
            "order_asc": "start_date",
            "queries": [{"field": "is_top", "type": "equal", "value": True}, {"field": "blv", "type": "not_equal", "value": None}]
        }
        
        try:
            response = page.request.post(
                api_url, 
                data=json.dumps(payload),
                headers={
                    "Content-Type": "application/json",
                    "Origin": "https://sv1.tieulamwc1.com",
                    "Referer": "https://sv1.tieulamwc1.com/",
                    "Accept": "application/json, text/plain, */*"
                }
            )
            
            if response.ok:
                data = response.json()
                browser.close()
                return data
            else:
                print(f"API phản hồi lỗi HTTP: {response.status}")
                print(f"Nội dung lỗi: {response.text()}")
        except Exception as e:
            print(f"Lỗi khi gửi yêu cầu API: {e}")
            
        browser.close()
        return None

# Xử lý kết quả
try:
    result = run()
    if result and 'data' in result:
        m3u_content = "#EXTM3U\n"
        count = 0
        for match in result.get('data', []):
            if match.get('source_live'):
                m3u_content += f"#EXTINF:-1, {match.get('title')}\n{match.get('source_live')}\n"
                count += 1
        
        if count > 0:
            with open('bongda.m3u', 'w', encoding='utf-8') as f:
                f.write(m3u_content)
            print(f"Xong! Đã lưu {count} trận.")
        else:
            print("API trả về nhưng không có link.")
    else:
        print("Kết quả trả về trống (None).")
except Exception as e:
    print(f"Lỗi script: {e}")
