import requests
from bs4 import BeautifulSoup

r = requests.get("https://tw.stock.yahoo.com/quote/2330.TW")
soup = BeautifulSoup(r.text, 'html.parser')

price         = soup.find('span', class_='Fw(600) Fz(16px)--mobile Fz(14px) D(f) Ai(c) C($c-trend-up)')
open_price    = price.find_next('span', class_='Fw(600) Fz(16px)--mobile Fz(14px) D(f) Ai(c) C($c-trend-up)')
highest_price = open_price.find_next('span', class_='Fw(600) Fz(16px)--mobile Fz(14px) D(f) Ai(c) C($c-trend-up)')
lowest_price  = highest_price.find_next('span', class_='Fw(600) Fz(16px)--mobile Fz(14px) D(f) Ai(c) C($c-trend-up)')

print(f'成交價:{price.text}\n開盤價:{open_price.text}\n最高價:{highest_price.text}\n最低價:{lowest_price.text}')