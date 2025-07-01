from fastapi import HTTPException, status, APIRouter
from ..schemas import UserResponse, UserLogin
from .. import models
from ..utils import hash, verify
from ..database import SessionDep


router = APIRouter(prefix="/auth", tags=["Authorization"])


@router.post("/register", status_code=status.HTTP_201_CREATED)
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
async def login_user(user_credentials: UserLogin, session: SessionDep):
    # Check email
    user: models.DBUser = (
        session.query(models.DBUser)
        .filter(models.DBUser.email == user_credentials.email)
        .first()
    )

    if not user:
        raise HTTPException(status_code=400, detail="Invalid credentials")

    # Check password
    pw_match = verify(user_credentials.password, user.password)
