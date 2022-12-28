# import enchant
import requests
from app import db


# this doesn't work rn, enchant doesn't work on silicon
# def check_spelling(key_term: str) -> tuple[bool, str]:
#     """
#
#     Args:
#         key_term:
#
#     Returns:
#         has_error, error_message
#     """
#     has_error = False
#     error_message = ""
#
#     dictionary = enchant.Dict("en_US")
#     if not dictionary.check(key_term):
#         has_error = True
#         error_message = f"Did you mean {dictionary.suggest(key_term)[0]}?"
#
#     return has_error, error_message


def isbn(isbn: str) -> tuple[bool, str]:
    """

    Args:
        isbn:

    Returns:
        has_error, error_message
    """
    if len(isbn) != 13:
        return True, "ISBN must be 13 characters, no spaces or hyphens."

    query = 'isbn:' + isbn
    params = {"q": query}
    url = r'https://www.googleapis.com/books/v1/volumes'

    response = requests.get(url, params=params)
    response_dict = response.json()
    try:
        print(response_dict['items'])
    except KeyError:
        return True, "ISBN is not valid."

    return False, ""


def title(book_title: str, author: str = None) -> tuple[bool, str, str]:
    """

    Args:
        author:
        book_title:

    Returns:
        has_error, error_message
    """
    if author:
        query = f'intitle:{book_title}+inauthor:{author}'
    else:
        query = f'intitle:{book_title}'
    params = {"q": query}
    url = r'https://www.googleapis.com/books/v1/volumes'

    response = requests.get(url, params=params)
    response_dict = response.json()
    found_isbn = "1234567891011"

    current = -1
    blacklist = db.get_blacklist()
    while found_isbn in blacklist:
        current += 1
        try:
            isbn_type = response_dict['items'][current]['volumeInfo']['industryIdentifiers'][0]['type']
            if isbn_type == "ISBN_13":
                found_isbn = response_dict['items'][current]['volumeInfo']['industryIdentifiers'][0]['identifier']
        except KeyError:
            return True, "Couldn't find a book with that title and author, please check spelling and try again.", ""
    return False, "", found_isbn
