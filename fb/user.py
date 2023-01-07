import pyrebase
import json

config = pyrebase.initialize_app(json.load(open('fb/fbconfig.json')))
database = config.database()


def sign_in(email: str, password: str) -> [bool, str]:
    try:
        user = config.auth().sign_in_with_email_and_password(email, password)
        return True, user["idToken"]
    except:
        return False


def register(email: str, password: str) -> bool:
    try:
        user = config.auth().create_user_with_email_and_password(email, password)
        return True
    except:
        return False