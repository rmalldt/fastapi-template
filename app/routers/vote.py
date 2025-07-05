from operator import and_
from typing import Annotated
from fastapi import Depends, HTTPException, Response, status, APIRouter
from ..schemas import PostOut, PostBase, TokenData, VoteIn
from .. import oauth2, models
from ..database import SessionDep
from sqlalchemy import select


router = APIRouter(prefix="/votes", tags=["Vote"])


@router.post(path="", status_code=status.HTTP_201_CREATED)
async def create_vote(
    vote: VoteIn,
    session: SessionDep,
    user: Annotated[models.UserAccount, Depends(oauth2.get_current_user)],
):

    stmt = select(models.UserAccount).where(models.UserAccount.id == 1)
    res = session.scalar(stmt)
    print(res)
    return res
