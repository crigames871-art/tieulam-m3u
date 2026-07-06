import requests
from bs4 import BeautifulSoup
import re

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
    'Referer': 'https://tieulam.co/'
}
trang_chu = "https://tieulam.co"

try:
    response = requests.get(trang_chu, headers=headers, timeout=15)
    soup = BeautifulSoup(response.text, 'html.parser')
    
    # Lấy tất cả các thẻ liên kết trên trang
    danh_sach_tran_dau = soup.find_all('a')
    
    m3u_content = "#EXTM3U\n"
    cac_link_da_quet = set() # Tránh trùng lặp trận đấu

    print(f"Tìm thấy tổng cộng {len(danh_sach_tran_dau)} liên kết trên trang chủ.")

    for tran in danh_sach_tran_dau:
        link_tran = tran.get('href', '')
        if not link_tran or link_tran in cac_link_da_quet:
            continue
            
        # Kiểm tra nếu link dẫn tới một trang con (bỏ qua link nhảy trang chủ hoặc link ngoài)
        if link_tran.startswith('/') or trang_chu in link_tran:
            if link_tran == '/' or link_tran == trang_chu:
                continue
                
            cac_link_da_quet.add(link_tran)
            if not link_tran.startswith('http'):
                link_tran = trang_chu + link_tran
                
            try:
                # Quét vào bên trong trang chi tiết của trận đấu
                chi_tiet = requests.get(link_tran, headers=headers, timeout=5)
                # Tìm luồng m3u8 ẩn bên trong
                match = re.search(r'(https?://[^\s"\'<>]+?\.m3u8[^\s"\'<>]*)', chi_tiet.text)
                
                if match:
                    ten_tran = tran.text.strip() or "Trực tiếp Bóng Đá"
                    link_m3u8 = match.group(1)
                    
                    m3u_content += f"#EXTINF:-1, {ten_tran}\n"
                    m3u_content += f"#EXTVLCOPT:http-referrer={trang_chu}\n"
                    m3u_content += f"{link_m3u8}\n"
                    print(f"Đã bắt được trận: {ten_tran}")
            except:
                continue

    # Ghi file
    with open('bongda.m3u', 'w', encoding='utf-8') as f:
        f.write(m3u_content)
    print("Quá trình quét hoàn tất!")

except Exception as e:
    print(f"Lỗi hệ thống: {e}")
