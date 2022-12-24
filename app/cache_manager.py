from dataclasses import asdict
import redis
from app.models import Book

r = redis.Redis(host='localhost', port=6379)


def check(key: str) -> bool:
    """Takes a key and checks if it exists in cache

    Args:
        key (str): isbn
    Returns:
        bool: exists in cache or not
    """
    return r.exists(key) == 1


def set(key: str, value: Book):
    value = str(value)
    r.setex(key, 172800, value)


def get(key: str) -> dict:
    """Takes the key and returns the book object in a string

    Args:
        key (str): isbn or title

    Returns:
        list[str]: book object in a string
    """
    decoded = r.get(key).decode('UTF-8')
    print(decoded)
    if isinstance(decoded, Book):
        return asdict(decoded)
    print("get", decoded)
    return decoded


def get_all() -> dict:
    """Gets all keys and values stored in cache

    Returns:
        list[dict]: list of dictionary items by key
    """
    # get keys
    keys = r.keys()
    
    # get values
    values = dict()
    for key in keys:
        values[key] = get(key)

    print(values)
    
    return values
