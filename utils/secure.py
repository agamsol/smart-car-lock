import os
from jose import JWTError, jwt
from jose.exceptions import ExpiredSignatureError
from utils.logger import create_logger
from models.secure import TokenData, generate_random_password
from dotenv import load_dotenv, set_key
from datetime import datetime, timedelta, timezone

load_dotenv()

JWT_SECRET = os.getenv("JWT_SECRET", "<RANDOM_SECURE_STRING>")
JWT_ALGORITHM = os.getenv("JWT_ALGORITHM", "HS256")
JWT_ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("JWT_ACCESS_TOKEN_EXPIRE_MINUTES", "60"))

log = create_logger("SECURE", logger_name="ASA_SECURE")

if JWT_SECRET == "<RANDOM_SECURE_STRING>":

    JWT_SECRET = generate_random_password(length=99)

    set_key(
        dotenv_path=".env",
        key_to_set="JWT_SECRET",
        value_to_set=JWT_SECRET
    )

    log.critical("No JWT_SECRET specified. A new secret has been generated and saved to .env. Please note this down if needed.")

if not JWT_SECRET or JWT_SECRET == "<RANDOM_SECURE_STRING>":

    log.critical("Application startup failed: JWT_SECRET is not set or remains as default placeholder.")
    raise RuntimeError("JWT_SECRET is not set in .env")


class JWToken:

    @staticmethod
    async def create():

        expire = datetime.now(timezone.utc) + (timedelta(minutes=JWT_ACCESS_TOKEN_EXPIRE_MINUTES))

        encoded_data = {
            "exp": expire
        }

        log.debug(f"Generating JWT. Exp: {encoded_data['exp']}")

        encoded_jwt = jwt.encode(encoded_data, JWT_SECRET, algorithm=JWT_ALGORITHM)

        return encoded_jwt

    @staticmethod
    async def verify(access_token: str) -> TokenData:

        try:

            payload = jwt.decode(access_token, JWT_SECRET, algorithms=[JWT_ALGORITHM])

            log.debug(f"JWT verification successful, Exp: {payload.get('exp')}")

            return TokenData(
                exp=payload.get("exp")
            )

        except ExpiredSignatureError:

            log.debug("JWT verification failed: Token signature has expired.")
            raise ValueError("Could not validate credentials")

        except JWTError as e:

            log.debug(f"JWT verification failed. Error: {str(e)}")
            raise ValueError("Could not validate credentials")
