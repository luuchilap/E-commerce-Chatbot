import os
import time

import pandas as pd
from bs4 import BeautifulSoup
from loguru import logger
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import NoSuchElementException, ElementClickInterceptedException


URL = "https://fptshop.com.vn/may-tinh-xach-tay?muc-gia=duoi-10-trieu%2Ctu-15-20-trieu&sort=noi-bat"
WAIT_TIMEOUT = 5

chrome_options = Options()
chrome_options.add_argument("--incognito")
driver = webdriver.Chrome(options=chrome_options)

driver.get(URL)
while True:
    try:
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight - 1200);")
        button = driver.find_element(By.XPATH, "//button[contains(@class, 'Button_root') and contains(@class, 'Button_btnSmall') and contains(@class, 'Button_whitePrimary')]")
        #button = driver.find_element(By.XPATH, "//button[contains(text(), ' kết quả')]")
        print("Click `Xem Thêm` button")
        button.click()
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight - 1200);")
    except NoSuchElementException:
        print("Scraping completed!")
        break
    except ElementClickInterceptedException:
        print("Not clickable, retrying")
        time.sleep(WAIT_TIMEOUT)

time.sleep(WAIT_TIMEOUT)

page = BeautifulSoup(driver.page_source, features="html.parser")

items = page.find_all("div", {"class": "group flex h-full flex-col justify-between ProductCard_brandCard__VQQT8 ProductCard_cardDefault__km9c5"})
logger.info(f"Num of items: {len(items)}")

products = []
for item in items:
    try:
        product_name = item.find("h3", {"class": "ProductCard_cardTitle__HlwIo"}).get_text()
        product_price = item.find("p", {"class": "Price_currentPrice__PBYcv"}).get_text()
        products.append({"product_name": product_name, "product_price": product_price})
    except:
        print("Cannot extract")

df = pd.DataFrame.from_dict(products)

dest = os.path.join("data", "products_fpt.csv")
if os.path.exists(dest):
    df.to_csv(dest, mode="a", index=False, header=False)
else:
    df.to_csv(dest, mode="w", index=False, header=False)
