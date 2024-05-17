import requests
import re
import pandas as pd

api_data = []
r = requests.get('https://airtw.moenv.gov.tw/json/camera_ddl_pic/camera_ddl_pic_2024051708.json')
if r.status_code == 200:
    data = r.json()
    for d in data:
        if 'AQI' not in d['Name'] or d['Value'] == '鹿林山':
            continue
        
        result = re.search(r'(.+)\(AQI=(\d+)', d['Name'])   # r 表示所有字符都是真正要寫的，不然 \d 會組裝起來(組裝的例子：\n)
        name   = result.group(1)
        aqi    = int(result.group(2))
        api_data.append([name, aqi])

api_data = pd.DataFrame(api_data, columns = ['Name', 'API'])
api_data.to_excel('api.xlsx')