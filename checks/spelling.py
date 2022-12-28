# import enchant
import requests


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


def check_isbn(isbn: str) -> tuple[bool, str]:
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


check_isbn("1234567891011")