from fastapi import HTTPException, APIRouter
from ..schemas import UserResponse
from .. import models
from ..database import SessionDep


router = APIRouter(prefix="/users", tags=["User"])


@router.get("/{id}", response_model=UserResponse)
async def get_user(id: int, session: SessionDep):
    user = session.query(models.DBUser).filter(models.DBUser.id == id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user
