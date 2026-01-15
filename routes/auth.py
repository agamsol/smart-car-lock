import os
from typing import Annotated
from fastapi import APIRouter, HTTPException, status, Depends
from utils.secure import JWToken
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from models.secure import TokenData, Token, generate_random_password
from dotenv import load_dotenv

load_dotenv()

SERVER_ACCESS_USERNAME = os.getenv("SERVER_ACCESS_USERNAME", "admin")
SERVER_ACCESS_PASSWORD = os.getenv("SERVER_ACCESS_PASSWORD", generate_random_password(10))

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")

router = APIRouter()


async def authenticate_with_token(
    credentials: Annotated[str, Depends(oauth2_scheme)],
) -> TokenData:

    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )

    try:
        token_data = await JWToken.verify(credentials)
    except ValueError:
        raise credentials_exception

    return TokenData(
        exp=token_data.exp
    )


@router.post(
    "/login",
    response_model=Token,
    tags=["Authentication"]
)
async def login_for_access_token(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()]
):
    if form_data.username == SERVER_ACCESS_USERNAME and form_data.password == SERVER_ACCESS_PASSWORD:
        access_token = await JWToken.create()
        return Token(
            access_token=access_token,
            token_type="bearer"
        )

    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Incorrect username or password",
        headers={"WWW-Authenticate": "Bearer"},
    )


@router.post(
    "/token",
    response_model=TokenData
)
async def generate_token(
    token: Annotated[TokenData, Depends(authenticate_with_token)]
):
    return token
