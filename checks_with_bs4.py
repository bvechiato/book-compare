from bs4 import BeautifulSoup
from lxml import etree
import requests

def waterstones(bookISBN):
    waterstonesURL = "https://www.waterstones.com/books/search/term/" + bookISBN 
    print("waterstonesURL: " + waterstonesURL)

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
    print("wobURL: " + wobURL)

    data = requests.get(wobURL).text
    soup = BeautifulSoup(data, 'lxml')

    try:
        elem = soup.find(class_="price")
        price = [elem.text, wobURL]
    except:
        price = "unavailable"

    return price

def goodreads_with_ISBN(bookISBN):
    goodreadsURL = "https://www.goodreads.com/search?q=" + bookISBN

    data = requests.get(goodreadsURL).text
    soup = BeautifulSoup(data, 'lxml')

    dom = etree.HTML(str(soup))

    try:
        amazonURL = dom.xpath("//*[@id='__next']/div/main/div[1]/div[1]/div/div[2]/div[2]/div/div[1]/button")[0]

        print("amazonURL: " + amazonURL.get('href'))
        return amazonURL
    except:
        return "unavailable"

def goodreads_with_bookName(bookName):
    newBookName = ""
    for x in bookName:
        if x == ' ':
            x = '+'

        newBookName += x
    
    goodreadsURL = "https://www.goodreads.com/search?q=" + newBookName
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