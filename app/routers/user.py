from fastapi import HTTPException, status, APIRouter
from ..schemas import UserResponse, UserCreate
from .. import models
from ..utils import hash
from ..database import SessionDep


router = APIRouter(prefix="/users")


@router.post("/", status_code=status.HTTP_201_CREATED)
async def create_user(user_data: UserCreate, session: SessionDep):
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


@router.get("/{id}", response_model=UserResponse)
async def get_user(id: int, session: SessionDep):
    user = session.query(models.DBUser).filter(models.DBUser.id == id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user
