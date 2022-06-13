from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
import time

s=Service('/Users/bea/Documents/python/projects/bookcompare/chromedriver')

chrome_options = Options()
# chrome_options.add_argument("--headless")

def amazon(amazonURL):
    driver = webdriver.Chrome(service=s, options=chrome_options)
    # driver = webdriver.Chrome(service=s)
    try:
        driver.get(amazonURL)
    except:
        return "amazon feature broken"
    driver.fullscreen_window()

    start_time = time.time()

    try:
        WebDriverWait(driver, 3).until(EC.presence_of_element_located((By.ID, "sp-cc-accept"))).click()

        elem = WebDriverWait(driver, 1).until(EC.presence_of_element_located((By.ID, "price")))
        price = [elem.get_attribute("textContent"), amazonURL]
    except:
        price = "unavailable"

    print(time.time() - start_time) 
    return price

# print(amazon("https://www.amazon.co.uk/gp/product/1501139231/ref=x_gr_w_bb_sout?ie=UTF8&tag=x_gr_w_bb_sout_uk-21&linkCode=as2&camp=1634&creative=6738"))
