from dataclasses import dataclass
from checks import price, find
import cache_manager


def config_book(search_term):
    [book_title, search_url, author, isbn] = find.book_info(search_term)

    # get price
    waterstones_price, waterstones_url = price.waterstones(isbn)
    wob_price, wob_url = price.wob(isbn)
    blackwells_price, blackwells_url = price.blackwells(isbn)

    # create new book
    new_book = Book(isbn.strip(), book_title.strip(), author.strip(), search_url.strip(),
                    wob_price.strip(), waterstones_price.strip(), blackwells_price.strip(), wob_url.strip(),
                    waterstones_url.strip(), blackwells_url.strip())

    # set cache
    cache_manager.set(isbn, new_book)
    display_book = str(new_book).split(", ")

    return display_book


@dataclass
class Book:
    isbn: str
    title: str
    author: str
    url_search: str
    price_wob: str
    price_waterstones: str
    price_blackwells: str
    url_wob: str
    url_waterstones: str
    url_blackwells: str
        
    def __str__(self):
        return f"{self.isbn}, {self.title}, {self.author}, {self.url_search}, {self.price_wob}, {self.price_waterstones}, {self.price_blackwells}, {self.url_wob}, {self.url_waterstones}, {self.url_blackwells}"
