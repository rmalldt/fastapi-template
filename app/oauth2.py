from typing import Annotated
from fastapi.security import OAuth2
import jwt
from jwt.exceptions import InvalidTokenError
from fastapi import Depends, status, HTTPException
from fastapi.security import OAuth2PasswordBearer
from datetime import datetime, timedelta, timezone
from .schemas import TokenData
from .database import SessionDep
from . import models
from .utils import verify_pw

SECRET_KEY = "09d25e094faa6ca2556c818166b7a9563b93f7099f6f0f4caa6cf63b88e8d3e7"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

# The parameter `tokenUrl` should be the user login endpoint which receives the user password
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/login")


def authenticate_user(username: str, password: str, session: SessionDep):
    user = session.query(models.DBUser).filter(models.DBUser.email == username).first()
    if not user:
        return False
    if not verify_pw(password, user.password):
        return False
    print(f"USER AUTHENTICATED: {user}")
    return user


def create_access_token(data: dict):
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    print(f"ACCESS TOKEN: {encoded_jwt}")
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
    except InvalidTokenError as err:
        raise credentials_exception
    return token_data


def get_current_user(token: Annotated[str, Depends(oauth2_scheme)]) -> TokenData:
    credential_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    return verify_access_token(token, credential_exception)
