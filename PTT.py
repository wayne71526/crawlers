import requests
from bs4 import BeautifulSoup
import pandas as pd

root_url = 'https://disp.cc'
r = requests.get("https://disp.cc/b/PttHot") # 與網址伺服器連線
soup = BeautifulSoup(r.text, 'html.parser') # 將 r.text 用 html.parser 解析

data = {
    'title':[],
    'href':[]
}

# 爬蟲
# 第一種方法
# spans = soup.find_all('span', class_="L34 nowrap listTitle")
# for span in spans:
#     if span.get('id') == 'title65112':
#         continue
#     data['title'].append(span.text)
#     data['href'].append(root_url+span.find('a').get('href'))


# 第二種方法 CSS selector
spans = soup.select('span.L34.nowrap.listTitle')
for span in spans:
    if span.find('a').get('href') == '/b/PttHot/59l9':
        continue
    data['title'].append(span.text)
    data['href'].append(root_url+span.find('a').get('href'))

    
# 將資料存成 excel 檔
data = pd.DataFrame(data)
data.to_excel('ptt.xlsx')