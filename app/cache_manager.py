import redis

r = redis.Redis(host='localhost', port=6379)


def check(key: str) -> bool:
    """Takes a key and checks if it exists in cache
    Args:
        key (str): isbn or title
    Returns:
        bool: exists in cache or not
    """
    return r.exists(key) == 1


def set(key: str, value):
    value = str(value)
    r.setex(key, 172800, value)


def get(key: str) -> list[str]:
    """Takes the key and returns the book object in a string
    Args:
        key (str): isbn or title
    Returns:
        list[str]: book object in a string
    """
    decoded = r.get(key).decode('UTF-8')
    return decoded.split(", ")


def get_all() -> list[list[str]]:
    """Gets all keys and values stored in cache
    Returns:
        list[list[str]]: 2D list of all books stored in cache as strings in the format [[isbn, title, url_goodreads,
        price_wob, price_waterstones, price_blackwells, url_wob, url_waterstones, url_blackwells], [...]]
    """
    # get keys
    keys = r.keys()

    # get values
    values = []
    for key in keys:
        values.append(get(key))

    return values
