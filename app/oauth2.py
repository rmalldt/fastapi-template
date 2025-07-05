from typing import Annotated
from fastapi.security import OAuth2
import jwt
from jwt.exceptions import InvalidTokenError
from fastapi import Depends, status, HTTPException
from fastapi.security import OAuth2PasswordBearer
from datetime import datetime, timedelta, timezone

from sqlalchemy import select
from .schemas import TokenData
from .database import SessionDep
from .models import UserAccount
from .utils import verify_pw
from .config import settings

SECRET_KEY = settings.secret_key
ALGORITHM = settings.algorithm
ACCESS_TOKEN_EXPIRE_MINUTES = settings.access_token_expire_minutes


# The parameter `tokenUrl` should be the user login endpoint which receives the user password
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/login")


def authenticate_user(username: str, password: str, session: SessionDep):
    stmt = select(UserAccount).where(UserAccount.email == username)
    user = session.scalar(stmt)
    if not user:
        return None
    if not verify_pw(password, user.password):
        return None
    return user


def create_access_token(data: dict):
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


def verify_access_token(token: str, credentials_exception) -> TokenData:
    """
    The shape of payload => {'sub': 'subject', 'exp': expiration} where:
        - 'sub': Type str
        - 'expiration': Type int
    """
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        id: str = payload.get("sub")
        if id is None:
            raise credentials_exception
        token_data = TokenData(id=id)
    except InvalidTokenError:
        raise credentials_exception
    return token_data


def get_current_user(
    token: Annotated[str, Depends(oauth2_scheme)], session: SessionDep
) -> UserAccount:
    credential_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )

    token_data = verify_access_token(token, credential_exception)
    stmt = select(UserAccount).where(UserAccount.id == token_data.id)
    user = session.scalar(stmt)
    if user is None:
        raise credential_exception
    return user
