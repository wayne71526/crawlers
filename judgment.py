import os
import re
import time
import requests
from bs4 import BeautifulSoup, Comment
from requests.exceptions import ConnectionError
from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import pandas as pd
import random

choices = [180, 195, 200, 210, 225, 240]

def get_bs4_content(url):
    res = requests.get(url, verify=False)
    soup = BeautifulSoup(res.text, "html.parser")
    return soup

# 將這些標籤文字內容 text 以逗號全部連結起來，就是完整的判決書內容了。
def get_full_text(content):
    nodes = content.find("body").find_all("td")
    full_text = ",".join([node.text for node in nodes]) # node.text：每一個 td 的文字
    return full_text

def get_main_text(content):
    raw_text = content.find("body").find(
        "div", {"class": "text-pre text-pre-in"})
    sentences = raw_text.find_all(
        text=lambda text: isinstance(text, Comment))
    main_text = ",".join(sentences)
    return main_text

name = "臺灣桃園地方法院"
period = [
    (100, 11, 1, 108, 10, 31)
]

article_data = pd.DataFrame()
article_id = 0

for y1, m1, d1, y2, m2, d2 in period:
    driver = webdriver.Chrome('chromedriver')
    url = "https://judgment.judicial.gov.tw/FJUD/Default_AD.aspx"
    driver.get(url)

    # 案件類別
    # a = driver.find_element(By.ID, "vtype_V")
    # a.find_element(By.NAME, "jud_sys").click()

    # 搜尋日期
    while True:
        try:
            content = driver.find_element(By.ID, "dy1") # 起始年
            content.send_keys(y1)
            break
        except:
            print("無法定位")
            time.sleep(5)

    content = driver.find_element(By.ID, "dm1") # 起始月
    content.send_keys(m1)

    content = driver.find_element(By.ID, "dd1") # 起始日
    content.send_keys(d1)

    content = driver.find_element(By.ID, "dy2") # 迄止年
    content.send_keys(y2)

    content = driver.find_element(By.ID, "dm2") # 迄止月
    content.send_keys(m2)

    content = driver.find_element(By.ID, "dd2") # 迄止日
    content.send_keys(d2)
    
    # 裁判主文
    content = driver.find_element(By.NAME, "jud_jmain")
    content.send_keys("無罪")
    

    # 全文內容
    content = driver.find_element(By.NAME, "jud_kw")
    content.send_keys("交通事故")


    # 送出查詢
    driver.find_element(By.NAME, "ctl00$cp_content$btnQry").click()

    # 裁判法院，查詢結果會開啟於新分頁
    court = driver.find_element(By.PARTIAL_LINK_TEXT , name)
    actions = ActionChains(driver).move_to_element(court).key_down(Keys.CONTROL).key_down(
            Keys.SHIFT).click(court).key_up(Keys.CONTROL).key_up(Keys.SHIFT)
    actions.perform()

    # 轉換到新開的畫面
    handles = driver.window_handles
    driver.switch_to.window(handles[-1])
    time.sleep(0.5)

    page_url = driver.current_url
    page_num = 1 # 第一頁開始
    while True: 
        if page_num <= int(25):
            page_content = get_bs4_content(url=page_url)

            # 將查詢結果列表中所有判決的 url 預存下來
            article_urls = [
                    f'https://judgment.judicial.gov.tw/FJUD/{node.get("href")}'
                    for node in page_content.body.table.find_all("a", {"id": "hlTitle"})
                ]

            for article_url in article_urls:
                article_id  += 1
                content = get_bs4_content(url=article_url)
                main_text = get_main_text(content=content)
                full_text = get_full_text(content=content)
                row = pd.DataFrame({
                    "id": article_id,
                    "url": article_url,
                    "main_text": main_text,
                    "full_text": full_text
                }, index=[0]) # index 設成 0
                article_data = article_data.append(row, ignore_index=True)
                time.sleep(0.5)

            try:
                # get next_page_url and assign to page_url
                next_page_qurl = page_content.find(
                    "a", {"class": "page", "id": "hlNext"}).get("href")
                page_url = f'https://judgment.judicial.gov.tw/{next_page_qurl} & ot = in'
                
            except AttributeError:
                break

            page_num += 1
            time.sleep(random.choice([10, 13, 15, 17, 20, 30]))
        else:
            break
    time.sleep(random.choice(choices))

article_data.to_excel(name + "無罪判決書(90-108).csv", index=False, encoding='utf-8')