import requests


def with_isbn(book_isbn: str):
    """

    Args:
        book_isbn:

    Returns:
        title, author, google_dict
    """
    query = 'isbn:' + book_isbn
    params = {"q": query}
    url = r'https://www.googleapis.com/books/v1/volumes'

    response = requests.get(url, params=params)
    response_dict = response.json()

    author = response_dict['items'][0]["volumeInfo"]['authors'][0]
    title = response_dict['items'][0]["volumeInfo"]['title']
    return title, author, response_dict
