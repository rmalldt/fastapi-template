from operator import or_
from typing import Annotated
from fastapi import Depends, HTTPException, Response, status, APIRouter
from ..schemas import PostResponse, PostBase, TokenData
from .. import models, oauth2
from ..database import SessionDep


router = APIRouter(prefix="/posts", tags=["Post"])


@router.get("", response_model=list[PostResponse])
async def get_posts(
    session: SessionDep,
    user: Annotated[models.UserAccount, Depends(oauth2.get_current_user)],
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
    posts = (
        session.query(models.Post)
        .filter(models.Post.user_id == user.id)
        .filter(
            or_(
                models.Post.title.contains(search), models.Post.content.contains(search)
            )
        )
        .offset(skip)
        .limit(limit)
        .all()
    )

    if not posts:
        raise HTTPException(status_code=404, detail="No posts found")
    return posts


@router.post("", status_code=status.HTTP_201_CREATED, response_model=PostResponse)
async def create_posts(
    post_data: PostBase,
    session: SessionDep,
    user: Annotated[models.UserAccount, Depends(oauth2.get_current_user)],
):
    new_post = models.Post(**post_data.model_dump(), user_id=user.id)
    session.add(new_post)
    session.commit()
    session.refresh(new_post)
    return new_post


@router.get("/{id}", response_model=PostResponse)
async def get_post(
    id: int,
    session: SessionDep,
    user: Annotated[models.UserAccount, Depends(oauth2.get_current_user)],
):
    print(f"USER ID: {user.id}")
    post = (
        session.query(models.Post)
        .filter(models.Post.user_id == user.id)
        .filter(models.Post.id == id)
        .first()
    )
    if not post:
        raise HTTPException(status_code=404, detail="Post not found")
    return post


@router.put("/{id}", response_model=PostResponse)
async def update_post(
    id: int,
    post_data: PostBase,
    session: SessionDep,
    user: Annotated[models.UserAccount, Depends(oauth2.get_current_user)],
):
    post = session.query(models.Post).filter(models.Post.id == id).first()
    if not post:
        raise HTTPException(status_code=404, detail="Post not found")

    if post.user_id != user.id:
        raise HTTPException(
            status_code=401, detail="Not authorized to perform the requestes action"
        )

    # Update the post attributes
    for key, value in post_data.model_dump().items():
        setattr(post, key, value)

    session.commit()
    session.refresh(post)
    return post


@router.delete("/{id}")
async def delete_post(
    id: int,
    session: SessionDep,
    user: Annotated[models.UserAccount, Depends(oauth2.get_current_user)],
):
    post = session.query(models.Post).filter(models.Post.id == id).first()
    if not post:
        raise HTTPException(status_code=404, detail="Post not found")

    if post.user_id != user.id:
        raise HTTPException(
            status_code=401, detail="Not authorized to perform the requestes action"
        )

    session.delete(post)
    session.commit()
    return Response(status_code=204)
