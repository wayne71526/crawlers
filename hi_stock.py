import requests
import time
import pandas as pd

no   = input('欲查詢的股票代號：')
days = input('欲查詢的天數：')


r = requests.get('https://histock.tw/stock/chip/chartdata.aspx?no={}&days={}&m=dailyk,close,volume,mean5,mean10,mean20,mean60,mean120,mean5volume,mean20volume,k9,d9,rsi6,rsi12,dif,macd,osc'.format(no, days))
if r.status_code == 200:
    r = r.json()                                # r.json()：將 json 檔轉成字典
    daily_k = eval(r['DailyK'])                 # 因 list 為字串形式，故利用 eval() 將字串形式的 list 轉換成真正的 list 形式

    for i in range(len(daily_k)):
        date = daily_k[i][0]/1000
        date = time.localtime(date)             # 將 timestamp 轉換成所居住地區的時間
        date = time.strftime('%Y/%m/%d', date)  # 將時間以年/月/日的形式表示
        daily_k[i][0] = date
        
        
data = pd.DataFrame(daily_k, columns=['date', 'opened_price', 'highest_price', 'lowest_price', 'closed_price'])
data.to_excel('2330(台積電)_dailyk.xlsx')