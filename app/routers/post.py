from operator import or_
from turtle import pos
from typing import Annotated
from fastapi import Depends, HTTPException, Response, status, APIRouter
from sqlalchemy import func, select, update
from ..schemas import PostOut, PostBase, PostWithVoteOut
from .. import oauth2
from ..models import Post, UserAccount, Vote
from ..database import SessionDep


router = APIRouter(prefix="/posts", tags=["Post"])


@router.get(
    "",
    response_model=list[PostWithVoteOut],
    dependencies=[Depends(oauth2.get_current_user)],
)
async def get_posts(
    session: SessionDep,
    skip: int = 0,
    limit: int = 50,
    search: str = "",
):
    """
    This function depends on `oauth.get_current_user` that forces user to login
    otherwise will return `Unauthorized`.

    It calls `oauth.get_current_user` function which verifies the `access_token`.
    It passes the token which comes from the request. The token gets decoded, the
    user id is extracted and returned to this function.
    """
    stmt = (
        select(Post, func.count(Vote.post_id))
        .join(Vote, Post.id == Vote.post_id, isouter=True)
        .where(or_(Post.title.contains(search), Post.content.contains(search)))
        .group_by(Post.id)
        .offset(skip)
        .limit(limit)
    )

    posts = session.execute(stmt).all()
    if not posts:
        raise HTTPException(status_code=404, detail="No posts found")
    return [{"post": row[0], "votes": row[1]} for row in posts]


@router.post("", status_code=status.HTTP_201_CREATED, response_model=PostOut)
async def create_posts(
    post_data: PostBase,
    session: SessionDep,
    user: Annotated[UserAccount, Depends(oauth2.get_current_user)],
):
    new_post = Post(**post_data.model_dump(), user_id=user.id)
    session.add(new_post)
    session.commit()
    session.refresh(new_post)
    return new_post


@router.get(
    "/{id}",
    response_model=PostWithVoteOut,
    dependencies=[Depends(oauth2.get_current_user)],
)
async def get_post(id: int, session: SessionDep):
    stmt = (
        select(Post, func.count(Vote.post_id))
        .join(Vote, Post.id == Vote.post_id, isouter=True)
        .where(Post.id == id)
        .group_by(Post.id)
    )

    post = session.execute(stmt).one()
    if not post:
        raise HTTPException(status_code=404, detail="Post not found")
    return {"post": post[0], "votes": post[1]}


@router.put("/{id}", response_model=PostOut)
async def update_post(
    id: int,
    post_data: PostBase,
    session: SessionDep,
    user: Annotated[UserAccount, Depends(oauth2.get_current_user)],
):
    update_stmt = (
        update(Post)
        .where(Post.id == id, Post.user_id == user.id)
        .values(**post_data.model_dump())
        .returning(Post)
    )

    result = session.execute(update_stmt)
    session.commit()

    updated_post = result.scalar_one_or_none()
    if updated_post is None:
        raise HTTPException(status_code=404, detail="Post not found")
    return updated_post


@router.delete("/{id}")
async def delete_post(
    id: int,
    session: SessionDep,
    user: Annotated[UserAccount, Depends(oauth2.get_current_user)],
):
    stmt = select(Post).where(Post.id == id)
    post = session.scalar(stmt)
    if not post:
        raise HTTPException(status_code=404, detail="Post not found")

    if post.user_id != user.id:
        raise HTTPException(
            status_code=401, detail="Not authorized to perform the requestes action"
        )

    session.delete(post)
    session.commit()
    return Response(status_code=204)
