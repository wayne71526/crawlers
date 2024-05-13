from selenium import webdriver
from selenium.webdriver.common.by import By

timestamp = input('請輸入timestamp：')
driver = webdriver.Chrome('chromedriver.exe')  # 建立 Chrome 驅動器
driver.get('https://www.unixtimestamp.com/index.php')  # 進入目標網址
driver.maximize_window()  # 視窗最大化
search = driver.find_element(By.XPATH, '/html/body/div[3]/div[1]/div[3]/div/div[1]/div/div[1]/div/div/input') 
search.send_keys(timestamp)  # 於格子內填入欲搜尋的 timestamp
button = driver.find_element(By.XPATH, '/html/body/div[3]/div[1]/div[3]/div/div[1]/div/div[1]/div/button') 
button.click()  # 點擊 convert

gmt = driver.find_element(By.CLASS_NAME, 'gmt').text
local = driver.find_element(By.CLASS_NAME, 'local').text
gmt = ' '.join(gmt.split()[:-1])
local = ' '.join(local.split()[:-2])

print(f'GMT(格林威治標準時間)：{gmt}')
print(f'Your Time Zone：{local}')