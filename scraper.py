import requests
from bs4 import BeautifulSoup
import re

# Khung code cơ bản để lấy link
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)',
    'Referer': 'https://tieulam.co/'
}
trang_chu = "https://tieulam.co"

try:
    response = requests.get(trang_chu, headers=headers)
    soup = BeautifulSoup(response.text, 'html.parser')
    
    # TẠM THỜI: Do chưa rõ cấu trúc thực tế của web tieulam, 
    # đây là đoạn code giả định nó tìm tất cả các thẻ <a> (link)
    danh_sach_tran_dau = soup.find_all('a') 
    
    m3u_content = "#EXTM3U\n"
    
    for tran in danh_sach_tran_dau:
        link_tran = tran.get('href', '')
        if 'tran-dau' in link_tran or 'truc-tiep' in link_tran: # Lọc các link có vẻ là trận đấu
            ten_tran = tran.text.strip() or "Trận đấu chưa rõ tên"
            if not link_tran.startswith('http'):
                link_tran = trang_chu + link_tran
                
            chi_tiet = requests.get(link_tran, headers=headers)
            match = re.search(r'(https?://[^\s"\'<>]+?\.m3u8[^\s"\'<>]*)', chi_tiet.text)
            
            if match:
                m3u_content += f"#EXTINF:-1, {ten_tran}\n"
                m3u_content += f"#EXTVLCOPT:http-referrer={trang_chu}\n"
                m3u_content += f"{match.group(1)}\n"

    # Lưu file
    with open('bongda.m3u', 'w', encoding='utf-8') as f:
        f.write(m3u_content)
    print("Xong!")

except Exception as e:
    print(f"Có lỗi: {e}")
