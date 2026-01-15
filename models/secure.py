import string
import random
from typing import Optional
from pydantic import BaseModel, Field


def generate_random_password(length=10):

    custom_specials = "!#$%^&*()[];:<>=-?@_+|{}~"

    characters = string.ascii_letters + string.digits + custom_specials
    password = ''.join(random.choice(characters) for _ in range(length))
    return password


class UserLoginRequest(BaseModel):
    username: str = Field(..., min_length=2, max_length=32)
    password: str = Field(..., min_length=2, max_length=500)


def user_login_request(username: str, password: str):

    return UserLoginRequest(
        username=username,
        password=password
    )


class TokenData(BaseModel):
    exp: Optional[int] = None


class Token(BaseModel):
    access_token: str
    token_type: str
