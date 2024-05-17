from datetime import datetime, timedelta
from typing import Dict, Optional, Union

import jwt
import structlog
from fastapi.requests import Request
from fastapi.security import (
    HTTPAuthorizationCredentials,
    HTTPBearer,
    OAuth2PasswordBearer,
)
from passlib.context import CryptContext

from app.config.settings import settings
from app.core.exceptions import AuthError

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/token")

LOG = structlog.get_logger()


def hash_password(password: str):
    hashed = pwd_context.hash(password)
    return hashed


def verify_password(plain_password: str, hashed_password: str):
    return pwd_context.verify(plain_password, hashed_password)


def create_access_token(
    data: dict, expires_delta: Union[timedelta, None] = None
) -> (str, str):
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(
            minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES
        )
    payload = {"expires_at": expire.strftime(settings.DATETIME_FORMAT), **data}
    encoded_jwt = jwt.encode(payload, settings.SECRET_KEY, algorithm=settings.ALGORITHM)
    expiration_datetime = expire.strftime(settings.DATETIME_FORMAT)
    return encoded_jwt, expiration_datetime


def generate_access_token(user: Dict) -> (str, str):
    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    return create_access_token(
        data={"id": str(user.get("id"))}, expires_delta=access_token_expires
    )


def generate_refresh_token(user: Dict) -> (str, str):
    refresh_token_expires = timedelta(days=settings.REFRESH_TOKEN_EXPIRE_DAYS)
    return create_access_token(
        data={"id": str(user.get("id"))}, expires_delta=refresh_token_expires
    )


def decode_token(token: str) -> dict:
    try:
        decoded_token = jwt.decode(
            token, settings.SECRET_KEY, algorithms=settings.ALGORITHM
        )

        expires_at = datetime.fromisoformat(decoded_token["expires_at"])

        return decoded_token if expires_at >= datetime.utcnow() else None
    except Exception as e:
        LOG.error(e)
        return {}


class JWTBearer(HTTPBearer):
    def __init__(self, auto_error: bool = True):
        super(JWTBearer, self).__init__(auto_error=auto_error)
        # self.allowed_roles = allowed_roles

    async def __call__(self, request: Request):
        credentials: HTTPAuthorizationCredentials = await super(
            JWTBearer, self
        ).__call__(request)
        if credentials:
            if not credentials.scheme == "Bearer":
                raise AuthError(detail="Invalid authentication scheme.")
            if not self.verify_jwt(credentials.credentials):
                raise AuthError(detail="Invalid or expired token.")
            request.state.user = decode_token(credentials.credentials)
            return credentials.credentials
        else:
            raise AuthError(detail="Invalid authorization code.")

    def verify_jwt(self, jwt_token: str) -> bool:
        try:
            payload = decode_token(jwt_token)
        except Exception as e:
            LOG.error(e)
            return False

        if payload.get("expires_at") is None:
            return False

        expires_at: Optional[datetime] = datetime.fromisoformat(
            payload.get("expires_at")
        )
        if expires_at is None:
            return False

        return expires_at > datetime.utcnow()
