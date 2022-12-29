import requests


def with_isbn(book_isbn: str):
    """

    Args:
        book_isbn:

    Returns:
        title, author, google_dict
    """
    query = 'isbn:' + book_isbn
    params = {"q": query, "orderBy": "relevance", "printType": "books"}
    url = r'https://www.googleapis.com/books/v1/volumes'

    response = requests.get(url, params=params)
    response_dict = response.json()

    try:
        author = response_dict['items'][0]["volumeInfo"]['authors'][0]
    except KeyError:
        author = response_dict['items'][0]["volumeInfo"]['publisher']
    title = response_dict['items'][0]["volumeInfo"]['title']
    return title, author, response_dict


def with_title(title: str, author: str):
    """

    Args:
        author:
        title:

    Returns:
        title, author, google_dict
    """
    query = f"{title}+{author}"
    params = {"q": query, "orderBy": "relevance", "printType": "books", "langRestrict": "en"}
    url = r'https://www.googleapis.com/books/v1/volumes'

    response = requests.get(url, params=params)
    response_dict = response.json()

    try:
        author = response_dict['items'][0]["volumeInfo"]['authors'][0]
    except KeyError:
        author = response_dict['items'][0]["volumeInfo"]['publisher']
    title = response_dict['items'][0]["volumeInfo"]['title']
    return title, author, response_dict


# print(with_title("tell me how to be", "neel patel"))
print(with_isbn('9781250184962'))