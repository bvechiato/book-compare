from bs4 import BeautifulSoup
from lxml import etree
import requests
import cloudscraper


def blackwells(book_title: str) -> list[str]:
    """Scrapes the search result and returns the first

    Args:
        book_title (str): inputted by the user

    Returns:
        list[str]: [price, url]
    """
    scraper = cloudscraper.create_scraper()
    blackwellsURL = "https://blackwells.co.uk/bookshop/search/?keyword=" + book_title.replace(' ', '+') 
    print("waterstonesURL: " + blackwellsURL)

    data = scraper.get(blackwellsURL).content
    soup = BeautifulSoup(data, 'lxml')
    
    dom = etree.HTML(str(soup))

    # Find price
    try:
        try:
            price = dom.xpath("//*[@class='search-result']/ul[1]/li[1]/div/div[2]/div/ul/li[2]")[0]
        except:
            price = dom.xpath("//*[@class='search-result']/ul[1]/li[1]/div/div[2]/div/ul/li[1]")[0]
    except:
        return ["book unavailable", "https://blackwells.co.uk"]

    # Url
    try:
        url = dom.xpath("//*[@class='search-result']/ul[1]/li[1]/a/@href")[0]
    except:
        return [price.text, "https://blackwells.co.uk"]
    
    return [price.text, "https://blackwells.co.uk" + url]
    

def waterstones(book_title: str) -> list[str]:
    """Scrapes the search result and returns the first

    Args:
        book_title (str): inputted by the user

    Returns:
        list[str]: [price, url]
    """
    scraper = cloudscraper.create_scraper()
    waterstonesURL = "https://waterstones.com/books/search/term/" + book_title.replace(' ', '+') 
    print("waterstonesURL: " + waterstonesURL)

    data = scraper.get(waterstonesURL).content
    soup = BeautifulSoup(data, 'lxml')
    
    dom = etree.HTML(str(soup))

    # Find price
    try:
        price = dom.xpath("//*[@class='search-results-list']/div[1]/div[1]/div[2]/div[2]/span[2]")[0]
    except:
        return ["book unavailable", "https://waterstones.com/"]

    # Url
    try:
        url = dom.xpath("//*[@class='search-results-list']/div[1]/div[1]/div[2]/span/a/@href")[0]
    except:
        return [price.text, "https://waterstones.com/"]
    
    return [price.text, "https://waterstones.com/" + url]


def wob(book_title: str) -> list[str]:
    """Scrapes the search result and returns the first

    Args:
        book_title (str): inputted by the user

    Returns:
        list[str]: [price, url]
    """
    scraper = cloudscraper.create_scraper()
    wobURL = "https://waterstones.com/books/search/term/" + book_title.replace(' ', '%20') 
    print("wobURL: " + wobURL)

    data = scraper.get(wobURL).content
    soup = BeautifulSoup(data, 'lxml')
    
    dom = etree.HTML(str(soup))

    # Find price
    try:
        price = dom.xpath("//*[@class='productList']/div[1]/div[1]/div[1]/div[2]")[0]
    except:
        return ["book unavailable", "https://wob.com/"]

    # Url
    try:
        url = dom.xpath("//*[@class='productList']/div[1]/div[1]/a[1]/@href")[0]
    except:
        return [price.text, "https://wob.com/"]
    
    return [price.text, "https://www.wob.com" + url]


# this needs to be reformatted
def goodreads(book_title: str) -> list[str]:
    """Scrapes the search result and returns the first's title

    Args:
        book_title (str): inputted by the user

    Returns:
        str: title
    """
    scraper = cloudscraper.create_scraper()
    goodreadsURL = "https://www.goodreads.com/search?q=" + book_title.replace(' ', '+') 
    print("goodreadsURL: " + goodreadsURL)

    data = scraper.get(goodreadsURL).content
    soup = BeautifulSoup(data, 'lxml')
    
    dom = etree.HTML(str(soup))

    # Find title
    try:
        title = dom.xpath("//table/tbody/tr[1]/td[1]/a/@title")[0]        
    except:
        return ["book unavailable", "https://www.goodreads.com"]
    
    # Find url
    try:
        url = dom.xpath("//table/tbody/tr[1]/td[1]/a/@href")[0]        
    except:
        return [title, "https://www.goodreads.com"]
    
    
    return [title, "https://www.goodreads.com" + url]
