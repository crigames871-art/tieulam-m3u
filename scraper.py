from playwright.sync_api import sync_playwright
import json
import time

def run():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        # Tạo context với User-Agent chuẩn để không bị chặn
        context = browser.new_context(
            user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36"
        )
        page = context.new_page()
        
        # Biến chứa dữ liệu
        captured_data = None

        # Thiết lập "cái lưới" lắng nghe phản hồi
        def on_response(response):
            nonlocal captured_data
            if "api.tlap17062026.com/matches/graph" in response.url:
                try:
                    # Chỉ lấy nếu là request thành công
                    if response.status == 200:
                        captured_data = response.json()
                except:
                    pass

        page.on("response", on_response)

        # Truy cập trang web và đợi nó load hoàn tất
        print("Đang truy cập và chờ tải dữ liệu...")
        try:
            page.goto("https://sv1.tieulamwc1.com/", wait_until="networkidle", timeout=60000)
            # Chờ thêm 5 giây để chắc chắn các yêu cầu API chậm được tải về
            page.wait_for_timeout(5000)
        except Exception as e:
            print(f"Lỗi khi truy cập: {e}")
        
        browser.close()
        return captured_data

try:
    data = run()
    
    # Kiểm tra xem có dữ liệu không
    if data and 'data' in data:
        m3u_content = "#EXTM3U\n"
        count = 0
        for match in data.get('data', []):
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
            print("Không tìm thấy link source_live.")
            with open('bongda.m3u', 'w', encoding='utf-8') as f:
                f.write("#EXTM3U\n#EXTINF:-1, Khong tim thay link\nhttp://error.com")
    else:
        print("Không bắt được dữ liệu API (data là None).")
        with open('bongda.m3u', 'w', encoding='utf-8') as f:
            f.write("#EXTM3U\n#EXTINF:-1, Khong lay duoc du lieu API\nhttp://error.com")

except Exception as e:
    with open('bongda.m3u', 'w', encoding='utf-8') as f:
        f.write(f"#EXTM3U\n#EXTINF:-1, Loi he thong: {str(e)[:50]}\nhttp://error.com")
