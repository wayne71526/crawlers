from bs4 import BeautifulSoup
import requests
from pprint import pprint
from datetime import datetime, timedelta


def crawler(date):
    r = requests.get('https://www.taifex.com.tw/cht/3/futContractsDate?queryDate={}%2F{}%2F{}'.format(date.year, date.month, date.day))
    if r.status_code == requests.codes.ok:
        soup = BeautifulSoup(r.text, 'html.parser')
    else:
        print('We can not connect the website')
    try:
        table = soup.find('table', class_='table_f table-fixed w-1000')
        trs   = table.find_all('tr', class_='12bk')[3:-4]
        print('We can get', date.strftime('%Y-%m-%d'))
    except AttributeError:
        print('We can not get', date.strftime('%Y-%m-%d'))
        return
    
    data = {}
    header = ['交易多方口數', '交易多方契約金額', '交易空方口數', '交易空方契約金額', '交易多方淨額口數', '交易多方淨額契約金額',
             '未平倉餘額多方口數', '未平倉餘額多方契約金額', '未平倉餘額空方口數', '未平倉餘額空方契約金額', '未平倉餘額多方淨額口數', 
             '未平倉餘額多方淨額契約金額']
    for tr in trs:
        tds = tr.find_all('td')
        if len(tds) == 15:
            product = tds[1].text.strip()
            row_data = [td.text.strip() for td in tds[1:]]
        else:
            row_data = [product] + [td.text.strip() for td in tds]
        
        # product -> who -> what        
        who = row_data[1]
        row_data = [int(d.replace(',', '')) for d in row_data[2:]]
        row_data = {header[i]:row_data[i] for i in range(len(header))}
        
        if product not in data:
            data[product] = {who:row_data}
        else:
            data[product][who] = row_data
    return data
    
days = 3
whole_data = {}
date = datetime.now()
while True:
    data = crawler(date)
    whole_data[date.strftime('%Y-%m-%d')] = data
    date = date - timedelta(days=1)
    if date < date.now() - timedelta(days=days):
        break
pprint(whole_data)