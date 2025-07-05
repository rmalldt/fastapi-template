from fastapi import HTTPException, APIRouter
from sqlalchemy import select
from ..schemas import UserOut
from ..models import UserAccount
from ..database import SessionDep


router = APIRouter(prefix="/users", tags=["User"])


@router.get("", response_model=list[UserOut])
async def get_users(session: SessionDep, limit=100):
    stmt = select(UserAccount).limit(limit)
    users = session.scalars(stmt)
    if not users:
        raise HTTPException(status_code=404, detail="Users not found")
    return users


@router.get("/{id}", response_model=UserOut)
async def get_user(id: int, session: SessionDep):
    stmt = select(UserAccount).where(UserAccount.id == id)
    user = session.scalar(stmt)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user
