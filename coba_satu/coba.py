from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, WebDriverException
from bs4 import BeautifulSoup
import pandas as pd
import time



opsi = webdriver.ChromeOptions()
opsi.add_argument('--headless')
servis = Service('chromedriver.exe')
driver = webdriver.Chrome(service = servis, options = opsi)

shopee_link = "https://shopee.co.id/search?keyword=macbook"

driver.set_window_size(1300, 800)
driver.get(shopee_link)


rentang = 500
for i in range(1,9):
    akhir = rentang * i
    perintah = "window,scrollTo(0, "+str(akhir)+")"
    driver.execute_script(perintah)
    print("loading ke-"+ str(i))
    time.sleep(1)
    
time.sleep(5)
list_nama, list_harga, list_link, list_terjual = [], [], [], []

driver.save_screenshot("home.png")
content = driver.page_source
driver.quit()
data = BeautifulSoup(content, 'html.parser')
#print(data.encode("utf-8"))

counter_page  = 0
i = 1
base_url = "https://shopee.co.id"
halaman = data.find('div', class_="shopee-page-controller")

while counter_page < 3:
    time.sleep(0.5)
    
    for area in data.find_all('div', class_= "col-xs-2-4 shopee-search-item-result__item"):
        print(i)
        nama = area.find('div', class_="ie3A+n bM+7UW Cve6sh").get_text()
        #gambar = area.find('img')['src'].get_text()
        harga = area.find('span', class_="ZEgDH9").get_text()
        terjual = area.find('div', class_="r6HknA uEPGHT")
        if terjual != None:
            terjual = terjual.get_text()
        link = base_url + area.find('a')['href']
        #driver.find_element_by_xpath("//button[@class='shopee-button-outline shopee-mini-page-controller__next-btn']").click()
        #driver.find_element("xpath", "//button[@class='shopee-button-outline shopee-mini-page-controller__next-btn']").click()
        print(nama)
        #print(gambar)
        list_nama.append(nama)
        list_harga.append(harga)
        list_link.append(link)
        list_terjual.append(terjual)
        print(harga)
        print(link)
        print(terjual)
        i +=1
        print("----")
        
    time.sleep(6)
    #next_page = driver.find_element(by=By.XPATH, value="//button[@class='css-1ix4b60-unf-pagination-item' and text()='" + str(counter_page + 1) + "']")
    counter_page += 1
    
    next_hal = driver.find_element(by=By.XPATH, value="//button[@class='shopee-button-no-outline' and text()='"+str(counter_page + 1) + "']")
   # next_page = data.find_element( by=By.XPATH, value="//*[@id='main']/div/div[2]/div/div/div[2]/div[2]/div[3]/div/button[8]")
    next_hal.click()
    #driver.find_element(by=By.XPATH, value="//*[@id='main']/div/div[2]/div/div/div[2]/div[2]/div[3]/div/button[8]").click()

df = pd.DataFrame({'Nama Produk':list_nama,
                  'harga':list_harga,
                  'link':list_link,
                  'terjual':list_terjual})

df.to_csv('scrape_shopee.csv')
    