from selenium.webdriver.common.by import By
from selenium import webdriver
import pandas as pd
import time
import traceback
import requests


class Scraper:
    def __init__(self):
        self.driver = webdriver.Firefox()

    def get_data(self):
        self.driver.get(
            'https://www.tokopedia.com/search?fcity=174%2C175%2C176%2C177%2C178%2C179%23144%2C146%2C150%2C151%2C167%2C168%2C171%2C174%2C175%2C176%2C177%2C178%2C179%2C463%23141%2C142%2C143%2C144%2C145%2C146%2C463%2C147%23253%2C254%2C255%2C256%2C257%23165%2C148%2C149%2C150%2C151%2C152%2C153%2C154%2C155%2C156%2C157%2C158%2C159%2C160%2C161%2C162%2C163%2C164%2C473%2C166%2C167%2C168%2C169%2C170%2C171%2C172%2C173%23180%2C181%2C182%2C183%2C184%2C185%2C186%2C187%2C188%2C189%2C190%2C191%2C192%2C193%2C194%2C195%2C196%2C197%2C198%2C199%2C200%2C201%2C202%2C203%2C204%2C205%2C206%2C207%2C208%2C209%2C210%2C211%2C213%2C214%2C212%23252%2C215%2C216%2C217%2C218%2C219%2C220%2C221%2C222%2C223%2C224%2C225%2C226%2C227%2C228%2C229%2C230%2C231%2C232%2C233%2C234%2C235%2C236%2C237%2C238%2C239%2C240%2C241%2C242%2C243%2C244%2C245%2C246%2C247%2C248%2C249%2C250%2C251&navsource=&page=1&q=PC&srp_component_id=01.07.00.00&srp_page_id=&srp_page_title=&st=product')

        counter_page = 0
        datas = []
        i = 1
        terjual_raw = 0

        try:
            while counter_page < 60:
                for _ in range(0, 5200, 400):
                    time.sleep(0.1)
                    self.driver.execute_script("window.scrollBy(0,450)")
                    time.sleep(1)

                elements = self.driver.find_elements(
                    by=By.CLASS_NAME, value='css-y5gcsw')
                for element in elements:
                    name = element.find_element(
                        by=By.CLASS_NAME, value='prd_link-product-name.css-3um8ox').text
                    name_fixed = name.replace(',', '-')
                    price = element.find_element(
                        by=By.CLASS_NAME, value='prd_link-product-price.css-1ksb19c').text
                    store = element.find_element(
                        by=By.CLASS_NAME, value='prd_link-shop-name.css-1kdc32b.flip').text
                    # city = element.find_element(by=By.CLASS_NAME, value='prd_link-shop-loc.css-1kdc32b.flip').text
                    city = element.find_element(
                        By.CLASS_NAME, value='prd_link-shop-loc.css-1kdc32b.flip').text
                    link = element.find_element(
                        by=By.TAG_NAME, value='a').get_attribute('href')

                    print("produk ke" + str(i))
                    try:
                        terjual_raw = element.find_element(
                            by=By.CLASS_NAME, value='prd_label-integrity.css-1duhs3e').text
                        terjual_fix = terjual_raw[8:]
                        terjual_fix = terjual_fix.replace('+', '')
                        terjual_fix = terjual_fix.replace('rb', '000')
                        terjual_fix = terjual_fix.replace(' ', '')
                    except:
                        print("Data terjual tidak ada")
                        terjual_fix = 0
                        pass

                    print("From", name.encode(
                        'cp1252', errors='ignore'), "To", name_fixed)
                    print(price)
                    print(store)
                    print(city)
                    print("from", terjual_raw, "to", terjual_fix)
                    print(link)
                    print("=========================")
                    i += 1

                    datas.append({
                        'Nama': name,
                        'Harga': price,
                        'Toko': store,
                        'Kota': city,
                        'terjual': terjual_fix,
                        'Link': link
                    })

                counter_page += 1
                next_page = self.driver.find_element(
                    by=By.XPATH, value="//button[@class='css-1ix4b60-unf-pagination-item' and text()='" + str(counter_page + 1) + "']")
                next_page.click()

        except:
            print("Error terjadi")
            traceback.print_exception()

        finally:
            df = pd.DataFrame(datas)

            df.to_csv("scrape_tokped_hal1.csv", index=False)
        return datas
