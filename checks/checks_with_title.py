from bs4 import BeautifulSoup
from lxml import etree
import requests
import cloudscraper


def blackwells(book_title: str):
    pass


def wob(book_title: str):
    pass


def waterstones(book_title: str):
    pass


# this needs to be reformatted
def goodreads(book_title: str) -> str:
    new_book_title = ""
    for x in book_title:
        if x == ' ':
            x = '+'

        newBookName += x
    
    goodreadsURL = "https://www.goodreads.com/search?q=" + new_book_title
    print("goodreadsURL: " + goodreadsURL)

    data = requests.get(goodreadsURL).text
    soup = BeautifulSoup(data, 'lxml')

    try:
        elem = soup.find(class_="bookTitle").get('href')

        bookURL = "https://www.goodreads.com/" + elem
        
        data2 = requests.get(bookURL).text
        soup2 = BeautifulSoup(data2, 'lxml')

        dom = etree.HTML(str(soup2))
        
        ISBN = dom.xpath("//*[@id='bookDataBox']/div[2]/div[2]/span/span")[0]
        print("ISBN: " + ISBN.text)

        return ISBN.text
    except:
        return "unavailable"
