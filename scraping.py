import os
import time

import pandas as pd
from bs4 import BeautifulSoup
from loguru import logger
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import NoSuchElementException, ElementClickInterceptedException


start_time = time.time()


WEBPAGE_URL = "https://product-management-tan.vercel.app/admin/products"
WAIT_TIME = 1
DATA_DIR = "data"
CSV_FILE = os.path.join(DATA_DIR, "products_info.csv")

# Setup Chrome options for incognito mode
chrome_options = Options()
chrome_options.add_argument("--incognito")
driver = webdriver.Chrome(options=chrome_options)
products_info = []
try:
    # URL
    driver.get(WEBPAGE_URL)
    #time.sleep(WAIT_TIME)

    # Locate the input element
    element = driver.find_element(By.XPATH, "//input[@type='email' and @id='email' and @name='email' and @class='form-control']")

    # Write text to the input field
    element.send_keys("t1@gmail.com")

    # Locate the password input element
    password_element = driver.find_element(By.XPATH, "//input[@type='password' and @id='password' and @name='password' and @class='form-control']")

    # Write "t1" to the password input field
    password_element.send_keys("t1")

    # Locate the "Log in" button
    login_button = driver.find_element(By.XPATH, "//button[@type='submit' and @class='btn btn-primary btn-block']")

    # Click the button
    login_button.click()

    # Locate the "Products" link
    products_link = driver.find_element(By.XPATH, "//a[@href='/admin/products']")

    # Click the link
    products_link.click()

    # Load items
    while True:
        try:
            # Scroll and scrape products
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            #Use BeautiSoup to parse the page
            page = BeautifulSoup(driver.page_source, "html.parser")
            products = page.find_all("tr", {"class": "product-info"})

            for product in products:
                try:
                    product_name = product.find("td", {"class": "product-title"}).get_text()
                    img_url = product.find("img")["src"]
                    product_price = product.find("td", {"class": "product-price"}).get_text()
                    product_update = product.find("td", {"class": "product-update"}).get_text()
                    products_info.append({"product_name": product_name, "img_url": img_url, "product_price": product_price, "product_update": product_update})
                except Exception as e:
                    logger.error(f"Cannot get product data: {e}")

            next_button = driver.find_element(By.XPATH, '//button[text()="Next"]')
            next_button.click()
            logger.info("Click `Next`")
        except NoSuchElementException:
            logger.info("Scraping completed!")
            break
        except ElementClickInterceptedException:
            logger.warning("Not clickable, retrying")
            time.sleep(WAIT_TIME)

    
finally:
    # Measure the end time and log total execution time
    end_time = time.time()
    logger.info(f"Time: {end_time - start_time:.2f} seconds")

    # Close
    driver.quit()


# Save to CSV
if not os.path.exists(DATA_DIR):
    os.makedirs(DATA_DIR)

df = pd.DataFrame(products_info)
df.to_csv(CSV_FILE, index=False)

execution_time = time.time() - start_time
logger.info(f"Execution time: {execution_time} seconds")