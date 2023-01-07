import pyrebase
import json

config = pyrebase.initialize_app(json.load(open('fbconfig.json')))
database = config.database()


def add_book(book_isbn: str, book_data: dict):
    database.child("Book").child(book_isbn).set(book_data)


def get_book(book_isbn: str) -> dict | None:
    book = database.child("Book").child(book_isbn).get().val()
    if not book:
        return None
    else:
        return book


def add_blacklist(book_isbn: str):
    database.child("Blacklist").push(book_isbn)


def get_blacklist() -> list[str]:
    packed = database.child("Blacklist").get().val()
    blacklist = [y for x, y in packed.items()]
    return blacklist


def is_in_blacklist(book_isbn: str) -> bool:
    return database.child("Blacklist").child(book_isbn).get().val()
