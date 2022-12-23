from bs4 import BeautifulSoup
from lxml import etree
import cloudscraper


def format_author(author):
    """
    Input comes in as "Surname, Forename"
    Args:
        author: author name

    Returns:
        Forename Surname
    """
    temp = author.split(", ")
    author = temp[1] + " " + temp[0]
    return author


def find(search_term: str) -> list[str]:
    """Scrapes the search result and returns the first's title

        Args:
            search_term (str): input by the user

        Returns:
            str: title
        """
    scraper = cloudscraper.create_scraper()
    isbn_search_url = "https://isbnsearch.org/search?s=" + search_term.replace(' ', '+')
    print("isbn_search_url: " + isbn_search_url)

    data = scraper.get(isbn_search_url).content
    soup = BeautifulSoup(data, 'lxml')

    dom = etree.HTML(str(soup))

    # Find ISBN
    try:
        # If we're taken to the search or product page
        isbn = dom.xpath("//*[@id='searchresults']/li[1]/div[2]/p[2]")[0]
        isbn = isbn.text[9::]
    except IndexError:
        return ["", "", "", ""]

    # Find title
    try:
        # If we're taken to search page
        found = dom.xpath("//*[@id='searchresults']/li[1]/div[2]/h2/a")[0]
        url = found.get("href")
        found = found.text
    except IndexError:
        return ["book unavailable", "", "", isbn]

    url = "https://isbnsearch.org" + url

    # Find author
    try:
        # If we're taken to the search or product page
        author = dom.xpath("//*[@id='searchresults']/li[1]/div[2]/p[1]")[0]
        author = format_author(author.text[8::])
    except IndexError:
        return [found, url, "", isbn]
    return [found, url, author, isbn]
