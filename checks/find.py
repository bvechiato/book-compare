from bs4 import BeautifulSoup
from lxml import etree
import requests
import cloudscraper

def title(search_term: str) -> list[str]:
    """Scrapes the search result and returns the first's title

    Args:
        book_title (str): inputted by the user

    Returns:
        str: title
    """
    scraper = cloudscraper.create_scraper()
    goodreadsURL = "https://www.goodreads.com/search?q=" + search_term.replace(' ', '+') 
    print("goodreadsURL: " + goodreadsURL)

    data = scraper.get(goodreadsURL).content
    soup = BeautifulSoup(data, 'lxml')
    
    dom = etree.HTML(str(soup))
    
    print(dom)

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
