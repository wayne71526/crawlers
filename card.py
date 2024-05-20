from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
import pandas as pd

CHROMEDRIVER = 'chromedriver.exe'
URL = 'https://ezweb.easycard.com.tw/search/CardSearch.php'
card_number = ''
birthday    = ''

class Card:
    def __init__(self):
        self.driver = webdriver.Chrome(CHROMEDRIVER)
    
    def run(self, card_number, birthday):
        self.get_website()                  # 進入網站
        self.enter_card_number(card_number)      # 輸入卡號
        self.enter_birthday(birthday)            # 輸入生日
        self.choose_time()
        self.enter_verification_number()
        self.search()
        self.get_data()
        
    def get_website(self):
        self.driver.get(URL)
        self.driver.maximize_window()
        
    def enter_card_number(self, card_number):
        card_number_input = self.driver.find_element(By.XPATH, '/html/body/form/div/div[1]/div[2]/div[2]/div/ul/li[1]/input')
        card_number_input.send_keys(card_number)
    
    def enter_birthday(self, birthday):
        birthday_input = self.driver.find_element(By.XPATH, '/html/body/form/div/div[1]/div[2]/div[2]/div/ul/li[2]/input')
        birthday_input.send_keys(birthday)
        
    def choose_time(self):
        time = self.driver.find_element(By.ID, 'date3m')
        time.send_keys(Keys.SPACE)
        
    def enter_verification_number(self):
        verification_number = input('請輸入驗證碼：')
        verification_number_input = self.driver.find_element(By.XPATH, '/html/body/form/div/div[1]/div[2]/div[2]/div/ul/li[4]/input')
        verification_number_input.send_keys(verification_number)
        
    def search(self):
        button = self.driver.find_element(By.ID, 'btnSearch')
        button.click()
    
    def get_data(self):
        rows = self.driver.find_elements(By.CLASS_NAME, 'r1')
        data = []
        for row in rows:
            data.append([td.text for td in row.find_elements(By.TAG_NAME, 'td')])
        header = ['交易時間', '交易類別', '交易場所', '交易金額', '餘額', '社福優惠', '北捷累積次數', '北捷累積金額',
                 '北結回饋金試算', '累積使用點數']
        data = pd.DataFrame(data, columns=header)
        data.to_excel('悠遊卡交易紀錄.xlsx')
            
    
if __name__ == '__main__':
    c = Card()
    c.run(card_number, birthday)