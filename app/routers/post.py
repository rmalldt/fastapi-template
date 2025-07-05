from operator import or_
from turtle import pos
from typing import Annotated
from fastapi import Depends, HTTPException, Response, status, APIRouter
from sqlalchemy import select
from ..schemas import PostOut, PostBase
from .. import oauth2
from ..models import Post, UserAccount
from ..database import SessionDep


router = APIRouter(prefix="/posts", tags=["Post"])


@router.get("", response_model=list[PostOut])
async def get_posts(
    session: SessionDep,
    user: Annotated[UserAccount, Depends(oauth2.get_current_user)],
    skip: int = 0,
    limit: int = 10,
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
        select(Post)
        .where(Post.user_id == user.id)
        .where(or_(Post.title.contains(search), Post.content.contains(search)))
        .offset(skip)
        .limit(limit)
    )

    posts = session.scalars(stmt)
    if not posts:
        raise HTTPException(status_code=404, detail="No posts found")
    return posts


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


@router.get("/{id}", response_model=PostOut)
async def get_post(
    id: int,
    session: SessionDep,
    user: Annotated[UserAccount, Depends(oauth2.get_current_user)],
):
    stmt = select(Post).where(Post.user_id == user.id, Post.id == id)
    post = session.scalar(stmt)
    if not post:
        raise HTTPException(status_code=404, detail="Post not found")
    return post


@router.put("/{id}", response_model=PostOut)
async def update_post(
    id: int,
    post_data: PostBase,
    session: SessionDep,
    user: Annotated[UserAccount, Depends(oauth2.get_current_user)],
):
    stmt = select(Post).where(Post.id == id)
    post = session.scalar(stmt)
    if not post:
        raise HTTPException(status_code=404, detail="Post not found")

    if post.user_id != user.id:
        raise HTTPException(
            status_code=401, detail="Not authorized to perform the request action"
        )

    for key, value in post_data.model_dump().items():
        setattr(post, key, value)

    session.commit()
    session.refresh(post)
    return post


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
