from pydantic import EmailStr
from enum import Enum

def is_valid_email(email):
    try:
        EmailStr().validate(email)
        return True
    except:
        return False


def api_user(user: dict):
    user.pop("password", None)
    user["_id"] = str(user["_id"])
    return user


class UserRole(str, Enum):
    """[summary]
        Used to manage users roles.
    [description]
        Simple enumeration to link the users roles.
    """
    candidate = "candidate"
    voter = "voter"
    admin = "admin"

    @staticmethod
    def is_valid(role):
        return role in UserRole.__members__
















class UserAccountStatus(str, Enum):
    """[summary]
        Used to manage users accounts status.
    [description]
        Simple enumeration to link the accounts status.
    """
    registered = "registered"
    validated = "validated"