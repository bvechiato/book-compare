from dataclasses import dataclass
from app.checks import find, price
from app import cache_manager, db


@dataclass
class Book:
    isbn: str
    title: str
    author: str
    price_wob: str
    price_waterstones: str
    price_blackwells: str
    url_wob: str
    url_waterstones: str
    url_blackwells: str
        
    def __str__(self) -> str:
        return f"{self.isbn}, {self.title}, {self.author}, {self.price_wob}, " \
               f"{self.price_waterstones}, {self.price_blackwells}, {self.url_wob}, " \
               f"{self.url_waterstones}, {self.url_blackwells}"

    def make_dict(self) -> dict:
        return {
                "ISBN": self.isbn,
                "Title": self.title,
                "Author": self.author,
                "Wob": {"Price": self.price_wob, "URL": self.url_wob},
                "Waterstones": {"Price": self.price_waterstones, "URL": self.url_waterstones},
                "Blackwells": {"Price": self.price_blackwells, "URL": self.url_blackwells}
            }


def config_book(isbn) -> Book:
    book_title, author, google_dict = find.with_isbn(isbn)

    # get price
    waterstones_price, waterstones_url = price.waterstones(isbn)
    wob_price, wob_url = price.wob(isbn)
    blackwells_price, blackwells_url = price.blackwells(isbn)
    is_blacklisted = db.is_in_blacklist(isbn)

    if waterstones_price == "unavailable" and wob_price == "unavailable" and blackwells_price == "unavailable" \
            and not is_blacklisted:
        db.add_blacklist(isbn)
        is_blacklisted = True

    # create new book
    new_book = Book(isbn.strip(), book_title.strip(), author.strip(),
                    wob_price.strip(), waterstones_price.strip(), blackwells_price.strip(), wob_url.strip(),
                    waterstones_url.strip(), blackwells_url.strip())

    # set cache
    if not is_blacklisted:
        cache_manager.set(isbn, new_book)
        db.add_book(isbn, new_book.make_dict())

    return new_book


def create_from_dict(book_dict: dict) -> Book:
    return Book(book_dict['ISBN'], book_dict['Title'], book_dict['Author'], book_dict['Wob']['Price'],
                book_dict['Waterstones']['Price'], book_dict['Blackwells']['Price'], book_dict['Wob']['URL'],
                book_dict['Waterstones']['URL'], book_dict['Blackwells']['URL'])


def create_from_str(book_str: str) -> Book:
    book_list = book_str.split(", ")
    return Book(book_list[0], book_list[1], book_list[2], book_list[3], book_list[4], book_list[5], book_list[6],
                book_list[7], book_list[8])
