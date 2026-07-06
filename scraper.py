import requests
import json

# Dán giá trị bạn copy được từ trình duyệt vào đây
CF_CLEARANCE_TOKEN = "DÁN_GIÁ_TRỊ_BẠN_VỪA_COPY_VÀO_ĐÂY"

api_url = "https://api.tlap17062026.com/matches/graph"

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36',
    'Cookie': f'cf_clearance=mYYLF70MqUVrULoGsVVzREccYRk5ncux.j9IccnAMPw-1783330709-1.2.1.1-s_hAoAjzhxZK80LLEFNzbbTfhgqaqUAKWjAtFHKBCIn6gFH6mCo88CyBiS.jFca_MTr_1mkQ14IoRgE26hNP3DlI2wNnLZKXNk7Q.i1IdgC2pYNzJW3oVDUESEjsb5V_qh_zeskA4qpFEfSLV3wYCOUCbWpZkv5EdiKcjkH1pZP.cXgOL8AMdtvRkUSjAp7AXVI7eZvsk4G5BzmpknpVe0z953cHQfDzSG7H340RjddyYCLP4vmgUCHzU0mQ18Ilnwf.axHOy4.4OB5FwFWmCLcO57GDBErFR9RV2Ffv2KIqRZrYUavyiqyxKgTCXOBNONZu4gwyj5vWlWCdNTvj.FJMriyEA..E31OfgIq9noe48a7ZQA4Noggxr5kYCOuODakTio3Hhy0DsKqPn5fC81LTk9TmaPTGz_mcgsHwnDYT2hP6Z0LOx2wPHwpx75ZMMzEg18JEepG4MgiQNYGQQSFNGNpid9AovLKBCV9bl1FF6EB1s_KHae7xZhZjbKtc',
    'Origin': 'https://sv1.tieulamwc1.com',
    'Referer': 'https://sv1.tieulamwc1.com/',
    'Content-Type': 'application/json'
}

payload = {
    "limit": 9, "page": 1, "order_asc": "start_date",
    "queries": [{"field": "is_top", "type": "equal", "value": True}, {"field": "blv", "type": "not_equal", "value": None}]
}

try:
    response = requests.post(api_url, headers=headers, json=payload, timeout=10)
    if response.status_code == 200:
        data = response.json()
        m3u_content = "#EXTM3U\n"
        for match in data.get('data', []):
            if match.get('source_live'):
                m3u_content += f"#EXTINF:-1, {match.get('title')}\n{match.get('source_live')}\n"
        
        with open('bongda.m3u', 'w', encoding='utf-8') as f:
            f.write(m3u_content)
        print("Thành công! Đã lấy dữ liệu bằng Cookie.")
    else:
        print(f"Lỗi: {response.status_code} - {response.text}")
except Exception as e:
    print(f"Lỗi kết nối: {e}")
