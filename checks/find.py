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
    
    # Find title
    try:
        # If we're taken to search page
        title = dom.xpath("//table/tr[1]/td[1]/a/@title")[0]       
    except:
        # if we're taken to the product page
        title = dom.xpath("//*[@id='bookTitle']")[0]
        title = title.text       
    else:
        return ["book unavailable", "https://www.goodreads.com"]
    
    # Find url
    try:
        # If we're taken to the search page
        url = dom.xpath("//table/tr[1]/td[1]/a/@href")[0]
        url = "https://www.goodreads.com" + url        
    except:
        # If we're taken to the product page
        url = goodreadsURL
    else:
        return [title, "https://www.goodreads.com"]
    
    # Find author
    try: 
        # If we're taken to the search or product page
        author = dom.xpath("//*[@class='authorName']/span")[0]
    except:
        return [title, url, ""]
    
    
    return [title, url, author.text]
