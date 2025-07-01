from typing import Annotated
from fastapi import Depends, HTTPException, status, APIRouter
from fastapi.security import OAuth2PasswordRequestForm
from app import oauth2
from ..schemas import UserResponse, UserLogin
from .. import models, oauth2
from ..utils import hash, verify
from ..database import SessionDep


router = APIRouter(prefix="/auth", tags=["Authorization"])


@router.post(
    "/register", status_code=status.HTTP_201_CREATED, response_model=UserResponse
)
async def register_user(user_data: UserLogin, session: SessionDep):
    user = (
        session.query(models.DBUser)
        .filter(models.DBUser.email == user_data.email)
        .first()
    )
    if user:
        raise HTTPException(status_code=400, detail="Email already exists")

    # Hash the password
    hashed_pass = hash(user_data.password)
    user_data.password = hashed_pass

    # Insert the user with hashed password to DB
    new_user = models.DBUser(**user_data.model_dump())
    session.add(new_user)
    session.commit()
    session.refresh(new_user)
    return new_user


@router.post("/login", status_code=status.HTTP_200_OK)
async def login_user(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
    session: SessionDep,
):
    # Check email
    user: models.DBUser = (
        session.query(models.DBUser)
        .filter(models.DBUser.email == form_data.username)
        .first()
    )

    if not user:
        raise HTTPException(status_code=404, detail="Invalid credentials")

    # Check password
    if not verify(form_data.password, user.password):
        raise HTTPException(status_code=404, detail="Invalid credentials")

    # Create a token
    access_token = oauth2.create_access_token(data={"user_id": user.id})
    return {"access_token": access_token, "token_type": "bearer"}
