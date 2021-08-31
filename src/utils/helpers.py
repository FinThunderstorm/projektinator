from uuid import uuid4
from bcrypt import gensalt, hashpw


def get_test_user():
    password_hash = hashpw(bytes('salasana', 'utf-8'), gensalt())
    user = {
        "user_id": str(uuid4()),
        "username": "username",
        "user_role": 1,
        "password_hash": password_hash,
        "firstname": "Firstname",
        "lastname": "Lastname",
        "email": "firstname.lastname@costco.com",
        "profile_image": "imagestringlocation",
    }
    return user
