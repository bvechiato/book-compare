# import enchant
import requests
from fb import db


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
    if len(isbn) != 13 and len(isbn) != 10:
        return True, "ISBN must be 10 or 13 characters, no spaces or hyphens."

    query = 'isbn:' + isbn
    params = {"q": query, "orderBy": "relevance", "printType": "books", "projection": "lite"}
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
        query = f'{book_title}+inauthor:{author}'
    else:
        query = f'{book_title}'
    params = {"q": query, "orderBy": "relevance", "printType": "books", "maxResults": "40"}
    url = r'https://www.googleapis.com/books/v1/volumes'

    response = requests.get(url, params=params)
    response_dict = response.json()
    found_isbn = "1234567891011"
    validated_isbn = isbn(found_isbn)

    current = -1
    blacklist = db.get_blacklist()
    print(response_dict)
    for current in range(len(response_dict["items"])):
        try:
            isbn_type = response_dict['items'][current]['volumeInfo']['industryIdentifiers'][0]['type']
            if isbn_type == "ISBN_13":
                found_isbn = response_dict['items'][current]['volumeInfo']['industryIdentifiers'][0]['identifier']
                validated_isbn = isbn(found_isbn)
                if not validated_isbn[0] and found_isbn not in blacklist:
                    break
        except KeyError:
            return True, "Couldn't find a book with that title and author, please check spelling and try again.", ""
        print(current)
    if validated_isbn[0]:
        return True, "Couldn't find a book with that title and author, please check spelling and try again.", ""
    return False, "", found_isbn
