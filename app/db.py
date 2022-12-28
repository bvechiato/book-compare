import pyrebase

config = {
  "apiKey": "AIzaSyCpvrUiLC3nnHVwxz8dkq6DgZIDziIiVq8",
  "authDomain": "book-compare-373011.firebaseapp.com",
  "databaseURL": "https://book-compare-373011-default-rtdb.europe-west1.firebasedatabase.app",
  "projectId": "book-compare-373011",
  "storageBucket": "book-compare-373011.appspot.com",
  "messagingSenderId": "19786307298",
  "appId": "1:19786307298:web:90eb6c79e219f6226430bb",
  "measurementId": "G-XLTVF4VS79"
}

firebase = pyrebase.initialize_app(config)
database = firebase.database()


def add_book(book_isbn: str, book_data: dict):
    database.child("Book").child(book_isbn).set(book_data)


def get_book(book_isbn: str) -> dict:
    return database.child("Book").child(book_isbn).get().val()


def add_blacklist(book_isbn: str):
    database.child("Blacklist").push(book_isbn)


def get_blacklist() -> list[str]:
    packed = database.child("Blacklist").get().val()
    blacklist = [y for x, y in packed.items()]
    return blacklist
