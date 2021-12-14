from bs4 import BeautifulSoup
from lxml import etree
import requests

def waterstones(bookISBN):
    waterstonesURL = "https://www.waterstones.com/books/search/term/" + bookISBN 

    data = requests.get(waterstonesURL).text
    soup = BeautifulSoup(data, 'lxml')

    dom = etree.HTML(str(soup))
    
    try:
        elem = dom.xpath("/html/body/div[1]/div[3]/div[2]/section[1]/div[2]/div[2]/div/div/div/div[1]/div/b[2]")[0]
    except:
        elem = soup.find(class_="price")
    finally:
        try: 
            price = [elem.text, waterstonesURL]
        except:
            price = "unavailable"

    return price

def wob(bookISBN):
    wobURL = "https://www.wob.com/en-gb/category/all?search=" + bookISBN

    data = requests.get(wobURL).text
    soup = BeautifulSoup(data, 'lxml')

    try:
        elem = soup.find(class_="price")
        price = [elem.text, wobURL]
    except:
        price = "unavailable"

    return price
