from operator import and_
from typing import Annotated
from fastapi import Depends, Response, status, APIRouter

from ..schemas import VoteIn, VoteOut
from .. import oauth2
from ..models import UserAccount, Vote
from ..database import SessionDep
from sqlalchemy import select, update
from sqlalchemy.orm import Session


router = APIRouter(prefix="/votes", tags=["Vote"])


@router.get(
    path="",
    response_model=list[VoteOut],
    dependencies=[Depends(oauth2.get_current_user)],
)
async def get_votes(session: SessionDep, limit=100):
    stmt = select(Vote).limit(limit)
    votes = session.scalars(stmt)
    return votes


@router.post(path="", status_code=status.HTTP_201_CREATED)
async def create_vote(
    vote: VoteIn,
    session: SessionDep,
    user: Annotated[UserAccount, Depends(oauth2.get_current_user)],
):
    stmt = select(Vote).where(Vote.post_id == vote.post_id, Vote.user_id == user.id)
    found_vote = session.scalar(stmt)
    if found_vote:
        # Delete if already voted
        session.delete(found_vote)
        session.commit()
        return Response(status_code=204)
    else:
        # Create new if not voted
        new_vote = Vote(user_id=user.id, post_id=vote.post_id)
        session.add(new_vote)
        session.commit()
        session.refresh(new_vote)
        return {"message": "Successfully added vote"}
