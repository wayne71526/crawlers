import requests
import pandas as pd

def crawler(page):
    r = requests.get('https://24h.pchome.com.tw/search/v4.3/all/results?q=%E6%9B%B2%E9%9D%A2%E8%9E%A2%E5%B9%95&page={}&sort=rnk/dc'.format(page))
    if r.status_code == 200:
        d = r.json()
        prods = d['Prods']
    
    return prods

data = {'prod':[], 'price':[], 'origin_price':[], 'describe':[]}
page = 1
while True:
    prods = crawler(page)
    if prods == [ ]:
        break
    for prod in prods:
        data['prod'].append(prod['Name'])
        data['price'].append(prod['Price'])
        data['origin_price'].append(prod['OriginPrice'])
        data['describe'].append(prod['Describe'])
    page += 1

data = pd.DataFrame(data)
data.to_excel('曲面螢幕.xlsx')