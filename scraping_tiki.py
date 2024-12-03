import os
import time

import pandas as pd
from bs4 import BeautifulSoup
from loguru import logger
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import NoSuchElementException, ElementClickInterceptedException


URL = "https://tiki.vn/"
WAIT_TIMEOUT = 5

chrome_options = Options()
chrome_options.add_argument("--incognito")
driver = webdriver.Chrome(options=chrome_options)

driver.get(URL)

time.sleep(3)
quit_button = driver.find_element(By.XPATH, "//img[@alt='close-icon' and contains(@class, 'styles__StyledImg')]")
quit_button.click()
while True:
    try:
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight - 2300);")
        time.sleep(WAIT_TIMEOUT)
        show_more_button = driver.find_element(By.XPATH, '//a[text()="Xem Thêm"]')
        print("Click `Xem Thêm` button")
        show_more_button.click()
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight - 2300);")
    except NoSuchElementException:
        print("Scraping completed!")
        break
    except ElementClickInterceptedException:
        print("Not clickable, retrying")
        time.sleep(WAIT_TIMEOUT)

time.sleep(WAIT_TIMEOUT)

page = BeautifulSoup(driver.page_source, features="html.parser")

items = page.find_all("span", {"class": "style__StyledItem-sc-15gcnmi-0 eOAwET"})
logger.info(f"Num of items: {len(items)}")

products = []
for item in items:
    try:
        product_name = item.find("h3", {"class": "style__NameStyled-sc-15gcnmi-5 jGCIHE"}).get_text()
        product_price = item.find("div", {"class": "price-discount__price"}).get_text()
        products.append({"product_name": product_name, "product_price": product_price})
    except:
        print("Either image's URL or product name can not be found, skipped!")

df = pd.DataFrame.from_dict(products)

dest = os.path.join("data", "products_tiki.csv")
if os.path.exists(dest):
    df.to_csv(dest, mode="a", index=False, header=False)
else:
    df.to_csv(dest, mode="w", index=False, header=False)
