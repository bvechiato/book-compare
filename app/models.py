class Book:
    def __init__(self, isbn, title, url_goodreads, price_wob, price_waterstones, price_blackwells,
                 url_wob, url_waterstones, url_blackwells):
        self.isbn = isbn  # 0
        self.title = title  # 1
        self.url_goodreads = url_goodreads  # 2
        self.price_wob = price_wob  # 3
        self.price_waterstones = price_waterstones  # 4
        self.price_blackwells = price_blackwells  # 5
        self.url_wob = url_wob  # 6
        self.url_waterstones = url_waterstones  # 7
        self.url_blackwells = url_blackwells  # 8
        
    def __str__(self):
        return f"{self.isbn}, {self.title}, {self.url_goodreads}, {self.price_wob}, {self.price_waterstones}, {self.price_blackwells}, {self.url_wob}, {self.url_waterstones}, {self.url_blackwells}"
