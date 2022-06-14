from bs4 import BeautifulSoup
from lxml import etree
import requests
import cloudscraper


def waterstone(bookISBN: str):
    scraper = cloudscraper.create_scraper()
    waterstonesURL = "https://www.waterstones.com/books/search/term/" + bookISBN 
    print("waterstonesURL: " + waterstonesURL)

    data = scraper.get(waterstonesURL).content
    soup = BeautifulSoup(data, 'lxml')

    dom = etree.HTML(str(soup))

    print(dom)
    
    try:
        elem = dom.xpath("//*[@itemprop='price']")[0]
    except:
        elem = soup.select_one("body > div.main-container > div.main-page.row > div:nth-child(2) > section.book-detail.span12.alpha.omega > div.span7.mobile-span12.alpha.tablet-alpha > div.book-actions > div > div > div > div.price > div > b")
    finally:
        try: 
            price = [elem.text, waterstonesURL]
        except:
            price = ["unavailable on waterstones", waterstonesURL]
        print(price)

    return price

def blackwells(bookISBN: str):
    scraper = cloudscraper.create_scraper()
    blackwellsURL = "https://blackwells.co.uk/bookshop/product/" + bookISBN 
    print("waterstonesURL: " + blackwellsURL)

    data = scraper.get(blackwellsURL).content
    soup = BeautifulSoup(data, 'lxml')

    dom = etree.HTML(str(soup))
    
    try:
        elem = dom.xpath("//*[@id='main-content']/div[2]/div[1]/div[2]/div/div[1]/div/ul/li[2]")[0]
    except:
        elem = soup.select_one("#main-content > div.product_page > div.container.container--50.u-relative > div:nth-child(2) > div > div.product__price > div > ul > li.product-price--current")
    finally:
        try: 
            price = [elem.text, blackwellsURL]
        except:
            price = ["unavailable on blackwells", blackwellsURL]
        print(price)

    return price

def wob(bookISBN: str):
    wobURL = "https://www.wob.com/en-gb/category/all?search=" + bookISBN
    print("wobURL: " + wobURL)

    data = requests.get(wobURL).content
    soup = BeautifulSoup(data, 'lxml')

    try:
        elem = soup.find(class_="price")
        price = [elem.text, wobURL]
    except:
        price = ["unavailable on wob", wobURL]

    return price

def goodreads(bookISBN: str):
    goodreadsURL = "https://www.goodreads.com/search?q=" + bookISBN

    data = requests.get(goodreadsURL).content.decode('utf-8')
    soup = BeautifulSoup(data, 'lxml')

    dom = etree.HTML(str(soup))

    try:
        bookTitle = dom.xpath("//*[@id='bookTitle']")[0].text

        return [bookTitle, goodreadsURL]
    except:
        return ["book doesn't exist", goodreadsURL]