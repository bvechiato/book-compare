from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
import time

s=Service('/Users/bia/bookcompare/chromedriver')

chrome_options = Options()
chrome_options.add_argument("--headless")

def findISBN(bookName):
    driver = webdriver.Chrome(service=s, options=chrome_options)

    findURL = "https://www.isbnsearch.org"
    driver.get(findURL)

    searchBar = WebDriverWait(driver, 20).until(EC.visibility_of_element_located((By.ID, "searchQuery")))
    searchBar.send_keys(bookName)
    searchBar.send_keys(Keys.RETURN)
    
    firstSearchResult = driver.find_element(By.XPATH, "//*[@id='searchresults']/li[1]/div[2]/h2/a") 
    foundISBN = firstSearchResult.get_attribute('href')

    driver.quit()
    return foundISBN[28:]

def amazon(bookISBN):
    driver = webdriver.Chrome(service=s, options=chrome_options)

    amazonURL = "https://www.amazon.co.uk/s?k={}&ref=nb_sb_noss".format(bookISBN)
    driver.get(amazonURL)

    start_time = time.time()
    
    try:
        WebDriverWait(driver, 2).until(EC.presence_of_element_located((By.ID, "sp-cc-accept"))).click()

        try:
            WebDriverWait(driver, 1).until(EC.presence_of_element_located((By.XPATH, "//*[@id='search']/div[1]/div[1]/div/span[3]/div[2]/div[1]/div/span/div/div/div[2]/div[2]/div/div/div[1]/h2/a"))).click()
        except:
            WebDriverWait(driver, 1).until(EC.presence_of_element_located((By.XPATH, "//*[@id='search']/div[1]/div[1]/div/span[3]/div[2]/div[2]/div/span/div/div/div[2]/div[2]/div/div/div[1]/h2/a"))).click()

        elem = WebDriverWait(driver, 2).until(EC.presence_of_element_located((By.XPATH, "//*[@id='corePrice_feature_div']/div/span/span[2]")))
        price = elem.get_attribute("textContent")
    except:
        price = "unavailable"

    print(time.time() - start_time) 
    driver.quit()
    return price

# print(findISBN("Good Economics for Hard Times"))
# print(amazon("9780141986197"))
