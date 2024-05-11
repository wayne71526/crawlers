from bs4 import BeautifulSoup
import requests
import pandas as pd

r = requests.get("https://chart.capital.com.tw/Chart/TWII/TAIEX11.aspx")
soup = BeautifulSoup(r.text, 'html.parser')
tables = soup.find_all('table', attrs={'cellpadding':'2'})
data = []

for table in tables:
    trs = table.find_all('tr')
    for tr in trs[1:]:
        date, value, price = [td.text for td in tr.find_all('td')]
        data.append([date, value, price])
        
data = pd.DataFrame(data, columns=['日期', '買賣超金額', '台指期'])
data.to_excel('big_eight.xlsx')