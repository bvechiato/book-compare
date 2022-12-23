from bs4 import BeautifulSoup
from lxml import etree
import cloudscraper


# def title(search_term: str) -> list[str]:
#     """Scrapes the search result and returns the first's title
#
#     Args:
#         search_term (str): input by the user
#
#     Returns:
#         str: title
#     """
#     scraper = cloudscraper.create_scraper()
#     goodreadsURL = "https://www.goodreads.com/search?q=" + search_term.replace(' ', '+')
#     print("goodreadsURL: " + goodreadsURL)
#
#     data = scraper.get(goodreadsURL).content
#     soup = BeautifulSoup(data, 'lxml')
#
#     dom = etree.HTML(str(soup))
#
#     # Find title
#     try:
#         # If we're taken to search page
#         found_title = dom.xpath("//table/tr[1]/td[1]/a/@title")[0]
#     except IndexError:
#         # if we're taken to the product page
#         try:
#             found_title = dom.xpath("//*[@id='bookTitle']")[0]
#             found_title = found_title.text
#         except IndexError:
#             return ["book unavailable", "https://www.goodreads.com", ""]
#
#     # Find url
#     try:
#         # If we're taken to the search page
#         url = dom.xpath("//table/tr[1]/td[1]/a/@href")[0]
#         url = "https://www.goodreads.com" + url
#     except IndexError:
#         # If we're taken to the product page
#         try:
#             url = goodreadsURL
#         except IndexError:
#             return [found_title, "https://www.goodreads.com", ""]
#
#     # Find author
#     try:
#         # If we're taken to the search or product page
#         author = dom.xpath("//*[@class='authorName']/span")[0]
#     except IndexError:
#         return [found_title, url, ""]
#     return [found_title, url, author.text]


def title(search_term: str) -> list[str]:
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
        return ["", "", "", "", ""]

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
        author = author.text[8::]
    except IndexError:
        return [found, url, "", isbn]
    return [found, url, author, isbn]
