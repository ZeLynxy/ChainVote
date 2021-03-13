from pydantic import EmailStr
from enum import Enum
from fastapi_mail import FastMail, MessageSchema, ConnectionConfig
from config.config import EMAIL_CONF

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

class EmailSender(FastMail):
    def __init__(self):
        super().__init__(EMAIL_CONF)

    async def send_message(self, subject, recipients, body):
        print(f"{subject=}, {recipients=}, {body=}")
        message = MessageSchema(
            subject=subject,
            recipients=recipients,
            body=body,
        )
        await super().send_message(message)

async def send_post_account_activation_email(email, voter_id):
    await EmailSender().send_message(
        "Confidential - Voter ID", 
        email,
        f"Your voter account has been approved. Here is your voter ID: {voter_id}. Keep it private!"
    )
