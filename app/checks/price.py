from bs4 import BeautifulSoup
from lxml import etree
import cloudscraper


def waterstones(search_term: str):
    """
        Args:
            search_term:

        Returns:
            [price, url]
        """
    scraper = cloudscraper.create_scraper()
    waterstonesURL = "https://www.waterstones.com/books/search/term/" + search_term.replace(' ', '+')
    print("waterstonesURL: " + waterstonesURL)

    data = scraper.get(waterstonesURL).content
    soup = BeautifulSoup(data, 'lxml')

    dom = etree.HTML(str(soup))

    try:
        elem = dom.xpath("//*[@itemprop='price']")[0]
        return [elem.text, waterstonesURL]
    except IndexError:
        elem = soup.select_one(
            "body > div.main-container > div.main-page.row > div:nth-child(2) > "
            "section.book-detail.span12.alpha.omega > div.span7.mobile-span12.alpha.tablet-alpha > div.book-actions > "
            "div > div > div > div.price > div > b")
        if elem is not None:
            return [elem.text, waterstonesURL]

    try:
        # if we're taken to the search page
        price = dom.xpath("//*[@class='search-results-list']/div[1]/div[1]/div[2]/div[2]/span[2]")[0]
        url = dom.xpath("//*[@class='search-results-list']/div[1]/div[1]/div[2]/span/a/@href")[0]
        return [price.text, "https://waterstones.com/" + url]
    except IndexError:
        return ["unavailable", waterstonesURL]


def blackwells(search_term: str):
    """
    Args:
        search_term:

    Returns:
        [price, url]
    """
    scraper = cloudscraper.create_scraper()
    blackwellsURL = "https://blackwells.co.uk/bookshop/search/?keyword=" + search_term.replace(' ', '+')
    print("blackwellsURL: " + blackwellsURL)

    data = scraper.get(blackwellsURL).content
    soup = BeautifulSoup(data, 'lxml')

    dom = etree.HTML(str(soup))
    
    try:
        # if we're taken to the product page
        elem = dom.xpath("//*[@id='main-content']/div[2]/div[1]/div[2]/div/div[1]/div/ul/li[2]")[0]
        return [elem.text, blackwellsURL]
    except IndexError:
        elem = soup.select_one("#main-content > div.product_page > div.container.container--50.u-relative > "
                               "div:nth-child(2) > div > div.product__price > div > ul > li.product-price--current")
        if elem is not None:
            return [elem.text, blackwellsURL]

    try:
        # if we're taken to the search page 
        price = dom.xpath("//*[@class='search-result']/ul[1]/li[1]/div/div[2]/div/ul/li[1]")[0]
        url = dom.xpath("//*[@class='search-result']/ul[1]/li[1]/a/@href")[0]
        return [price.text, "https://blackwells.co.uk" + url]
    except IndexError:
        return ["unavailable", blackwellsURL]


def wob(search_term: str):
    """
        Args:
            search_term:

        Returns:
            [price, url]
    """
    scraper = cloudscraper.create_scraper()
    wobURL = "https://www.wob.com/en-gb/category/all?search=" + search_term.replace(' ', '+')
    print("wobURL: " + wobURL)

    data = scraper.get(wobURL).content
    soup = BeautifulSoup(data, 'lxml')
    
    dom = etree.HTML(str(soup))

    # if taken to the product page
    elem = soup.find(class_="price")
    if elem is not None:
        return [elem.text, wobURL]

    try:
        price = dom.xpath("//*[@class='productList']/div[1]/div[1]/div[1]/div[2]")[0]
        url = dom.xpath("//*[@class='productList']/div[1]/div[1]/a[1]/@href")[0]
        return [price.text, "https://www.wob.com" + url]
    except IndexError:
        return ["unavailable", wobURL]

