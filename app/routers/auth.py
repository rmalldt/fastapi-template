from typing import Annotated
from fastapi import Depends, HTTPException, status, APIRouter
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy import select
from ..schemas import Token, UserOut, UserIn
from .. import oauth2
from ..models import UserAccount
from ..utils import hash_pw
from ..database import SessionDep


router = APIRouter(prefix="/auth", tags=["Authorization"])


@router.post("/register", status_code=status.HTTP_201_CREATED, response_model=UserOut)
async def register_user(user_data: UserIn, session: SessionDep):
    # Check email
    stmt = select(UserAccount).where(UserAccount.email == user_data.email)
    user = session.scalar(stmt)
    if user:
        raise HTTPException(status_code=400, detail="Email already exists")

    # Hash password
    hashed_pw = hash_pw(user_data.password)
    user_data.password = hashed_pw

    # Register user
    new_user = UserAccount(**user_data.model_dump())
    session.add(new_user)
    session.commit()
    session.refresh(new_user)
    return new_user


@router.post("/login", status_code=status.HTTP_200_OK, response_model=Token)
async def login_user(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
    session: SessionDep,
):
    user = oauth2.authenticate_user(form_data.username, form_data.password, session)
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )

    access_token = oauth2.create_access_token(data={"sub": str(user.id)})
    return {"access_token": access_token, "token_type": "bearer"}
