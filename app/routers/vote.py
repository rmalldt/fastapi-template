from typing import Annotated
from fastapi import Depends, HTTPException, Response, status, APIRouter
from ..schemas import PostResponse, PostBase, TokenData, VoteIn
from .. import oauth2, models
from ..database import SessionDep


router = APIRouter(prefix="/votes", tags=["Vote"])


@router.post(path="", status_code=status.HTTP_201_CREATED)
async def create_vote(
    vote: VoteIn,
    session: SessionDep,
    user: Annotated[models.UserAccount, Depends(oauth2.get_current_user)],
):
    print(vote.post_id, vote.direction)
