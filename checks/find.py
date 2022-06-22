from bs4 import BeautifulSoup
from lxml import etree
import requests
import cloudscraper

def info(search_term: str) -> list[str]:
    """Scrapes the search result and returns the first's title

    Args:
        book_title (str): inputted by the user

    Returns:
        list[str]: [book title, goodreads ulr, isbn]
    """
    scraper = cloudscraper.create_scraper()
    goodreadsURL = "https://www.goodreads.com/search?q=" + search_term.replace(' ', '+') 
    print("goodreadsURL: " + goodreadsURL)

    data = scraper.get(goodreadsURL).content
    soup = BeautifulSoup(data, 'lxml')
    
    dom = etree.HTML(str(soup))
    
    book_isbn = isbn(goodreadsURL)
    
    # Find title
    try:
        title = dom.xpath("//table/tr[1]/td[1]/a/@title")[0]       
    except:
        return ["book unavailable", "https://www.goodreads.com"]
    
    # Find url
    try:
        url = dom.xpath("//table/tr[1]/td[1]/a/@href")[0]        
    except:
        return [title, "https://www.goodreads.com"]
    
    
    return [title, "https://www.goodreads.com" + url]


def isbn(goodreads_url: str) -> str:
    scraper = cloudscraper.create_scraper()

    data = scraper.get(goodreads_url).content
    soup = BeautifulSoup(data, 'lxml')
    
    dom = etree.HTML(str(soup))
    
    try:
        isbn = dom.xpath("//*[@id='bookDataBox']/div[2]/div[2]/span/span")[0]
        return isbn.text       
    except:
        return ""
