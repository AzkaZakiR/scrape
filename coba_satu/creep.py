from selenium.webdriver.common.by import By
from selenium import webdriver
import pandas as pd
import time


class Scraper:
    def __init__(self):
        self.driver = webdriver.Firefox()

    def get_data(self):
        self.driver.get(
            'https://www.tokopedia.com/search?navsource=&ob=5&srp_component_id=02.01.00.00&srp_page_id=&srp_page_title=&st=product&q=sepatu')

        counter_page = 0
        datas = []
        i = 1

        while counter_page < 2:
            for _ in range(0, 5200, 400):
                time.sleep(0.1)
                self.driver.execute_script("window.scrollBy(0,400)")
                time.sleep(1)

            elements = self.driver.find_elements(
                by=By.CLASS_NAME, value='css-y5gcsw')
            for element in elements:
                # img = element.find_element(by=By.CLASS_NAME, value='css-1c345mg').get_attribute('src')
                # img = element.find_element(by=By.CLASS_NAME, value='css-1c345mg')['src']
                # price = element.find('div', class_='prd_link-product-price css-1ksb19c').text()
                # city = element.find('div', class_='prd_link-shop-loc css-1kdc32b flip').text()
                name = element.find_element(
                    by=By.CLASS_NAME, value='prd_link-product-name.css-3um8ox').text
                price = element.find_element(
                    by=By.CLASS_NAME, value='prd_link-product-price.css-1ksb19c').text
                city = element.find_element(
                    by=By.CLASS_NAME, value='prd_link-shop-loc.css-1kdc32b.flip').text
                print("produk ke" + str(i))
                print("produk ", name)
                print(price)
                print(city)
                i += 1

                datas.append({
                    # 'img': img,
                    'name': name,
                    'price': price,
                    'city': city
                })

            counter_page += 1
            next_page = self.driver.find_element(
                by=By.XPATH, value="//button[@class='css-1ix4b60-unf-pagination-item' and text()='" + str(counter_page + 1) + "']")
            next_page.click()

        df = pd.DataFrame(datas)

        df.to_csv("scrape_tokped.csv")
        return datas
