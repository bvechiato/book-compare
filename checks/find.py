import requests


def with_isbn(book_isbn: str):
    """

    Args:
        book_isbn:

    Returns:
        title, author, google_dict
    """
    query = 'isbn:' + book_isbn
    params = {"q": query, "orderBy": "relevance", "printType": "books", "projection": "lite"}
    url = r'https://www.googleapis.com/books/v1/volumes'

    response = requests.get(url, params=params)
    response_dict = response.json()
    print(book_isbn)
    print(response_dict)

    author = response_dict['items'][0]["volumeInfo"]['authors'][0]
    title = response_dict['items'][0]["volumeInfo"]['title']
    return title, author, response_dict


def with_title(title: str, author: str):
    """

    Args:
        book_isbn:

    Returns:
        title, author, google_dict
    """
    query = f'intitle:{title}+inauthor:{author}'
    params = {"q": query, "orderBy": "relevance", "printType": "books", "projection": "lite"}
    url = r'https://www.googleapis.com/books/v1/volumes'

    response = requests.get(url, params=params)
    response_dict = response.json()
    print(response_dict)

    author = response_dict['items'][0]["volumeInfo"]['authors'][0]
    title = response_dict['items'][0]["volumeInfo"]['title']
    return title, author, response_dict


with_isbn("9781398705241")
with_title("tell me how to be", "neel patel")
