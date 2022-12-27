import enchant


def check_spelling(key_term: str) -> tuple[bool, str]:
    """

    Args:
        key_term:

    Returns:
        has_error, error_message
    """
    has_error = False
    error_message = ""

    dictionary = enchant.Dict("en_US")
    if not dictionary.check(key_term):
        has_error = True
        error_message = f"Did you mean {dictionary.suggest(key_term)[0]}?"

    return has_error, error_message


def check_isbn(isbn: str) -> tuple[bool, str]:
    """

    Args:
        isbn:

    Returns:
        has_error, error_message
    """
    has_error = False
    error_message = ""

    if len(isbn) != 13:
        has_error = True
        error_message = "ISBN must be 13 characters, no spaces or hyphens."

    return has_error, error_message
