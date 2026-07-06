import requests

headers = {
    'accept': '*/*',
    'accept-language': 'vi,en;q=0.9',
    'content-type': 'application/json',
    'origin': 'https://sv1.tieulamwc1.com',
    'priority': 'u=1, i',
    'referer': 'https://sv1.tieulamwc1.com/trang-chu?__cf_chl_f_tk=CUrSTW1vAnMgA4iF8C.VQeRkjfeAMRdEPDX7bNqiCWg-1783333161-1.0.1.1-I_RFV6IvRmPaAS7gk1UMfRFRGvJwMtjZIaZj2DcDAm8',
    'sec-ch-ua': '"Chromium";v="146", "Not-A.Brand";v="24", "Google Chrome";v="146"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
    'sec-fetch-dest': 'empty',
    'sec-fetch-mode': 'cors',
    'sec-fetch-site': 'cross-site',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/146.0.0.0 Safari/537.36',
}

json_data = {
    'limit': 9,
    'page': 1,
    'order_asc': 'start_date',
    'queries': [
        {
            'field': 'is_top',
            'type': 'equal',
            'value': True,
        },
        {
            'field': 'blv',
            'type': 'not_equal',
            'value': None,
        },
    ],
}

response = requests.post('https://api.tlap17062026.com/matches/graph', headers=headers, json=json_data)

# Note: json_data will not be serialized by requests
# exactly as it was in the original request.
#data = '{"limit":9,"page":1,"order_asc":"start_date","queries":[{"field":"is_top","type":"equal","value":true},{"field":"blv","type":"not_equal","value":null}]}'
#response = requests.post('https://api.tlap17062026.com/matches/graph', headers=headers, data=data)
