from re import search
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service

s=Service('/Users/bia/bookcompare/chromedriver')
driver = webdriver.Chrome(service=s)

def findISBN(bookName):
    findURL = "https://www.isbnsearch.org"
    driver.get(findURL)

    searchBar = WebDriverWait(driver, 20).until(EC.visibility_of_element_located((By.ID, "searchQuery")))
    searchBar.send_keys(bookName)
    searchBar.send_keys(Keys.RETURN)
    
    firstSearchResult = driver.find_element(By.XPATH, "//*[@id='searchresults']/li[1]/div[2]/h2/a") 
    foundISBN = firstSearchResult.get_attribute('href')

    return foundISBN[28:]

def waterstones(bookISBN):
    waterstonesURL = "https://www.waterstones.com/books/search/term/" + bookISBN 
    driver.get(waterstonesURL)

    button = WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.XPATH, "//*[@id='onetrust-accept-btn-handler']")))
    driver.execute_script("arguments[0].click();", button)
    
    try:
        # print("tried 1")
        elem = WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.XPATH, "/html/body/div[1]/div[3]/div[2]/section[1]/div[2]/div[2]/div/div/div/div[1]/div/b[2]")))
        # print("worked")
    except:
        # print("tried 2")
        elem = WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.CLASS_NAME, "price")))
        # print("worked")
    finally:
        try: 
            price = elem.get_attribute("textContent")
        except:
            price = "unavailable"

    return price

def wob(bookISBN):
    wobURL = "https://www.wob.com/en-gb/category/all?search=" + bookISBN
    driver.get(wobURL)


    try:
        elem = WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.CLASS_NAME, "price")))
        price = elem.get_attribute("textContent")
    except:
        price = "unavailable"

    return price


def amazon(bookISBN):
    amazonURL = "https://www.amazon.co.uk/s?k={}&ref=nb_sb_noss".format(bookISBN)
    driver.get(amazonURL)

    try:
        WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.XPATH, "//*[@id='search']/div[1]/div[1]/div/span[3]/div[2]/div[1]/div/span/div/div/div[2]/div[2]/div/div/div[1]/h2/a"))).click()

        elem = WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.XPATH, "//*[@id='corePrice_feature_div']/div/span/span[2]")))
        price = elem.get_attribute("textContent")
    except:
        price = "unavailable"

    return price

# print(findISBN("Good Economics for Hard Times"))
# print(waterstones("9780141986197"))
# print(wob("9780141986197"))
# print(amazon("9780141986197"))
