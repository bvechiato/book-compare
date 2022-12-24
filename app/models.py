from dataclasses import dataclass


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
