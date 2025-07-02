from typing import Annotated
from fastapi import Depends, HTTPException, Response, status, APIRouter
from ..schemas import PostResponse, PostBase, TokenData
from .. import models, oauth2
from ..database import SessionDep


router = APIRouter(prefix="/posts", tags=["Post"])


@router.get("/", response_model=list[PostResponse])
async def get_posts(
    session: SessionDep,
    current_id: Annotated[TokenData, Depends(oauth2.get_current_user)],
):
    """
    This function depends on `oauth.get_current_user` that forces user to login
    otherwise will return `Unauthorized`.

    It calls `oauth.get_current_user` function which verifies the `access_token`.
    It passes the token which comes from the request. The token gets decoded, the
    user id is extracted and returned to this function.
    """
    if current_id.id:
        print(f"CURRENT ID: {int(current_id.id)}")
    posts = session.query(models.DBPost).all()
    if not posts:
        raise HTTPException(status_code=404, detail="No posts found")
    return posts


@router.post("/", status_code=status.HTTP_201_CREATED)
async def create_posts(
    post_data: PostBase,
    session: SessionDep,
    current_id: Annotated[TokenData, Depends(oauth2.get_current_user)],
):
    new_post = models.DBPost(**post_data.model_dump())
    session.add(new_post)
    session.commit()
    session.refresh(new_post)
    return new_post


@router.get("/{id}", response_model=PostResponse)
async def get_post(
    id: int,
    session: SessionDep,
    current_id: Annotated[TokenData, Depends(oauth2.get_current_user)],
):
    post = session.query(models.DBPost).filter(models.DBPost.id == id).first()
    if not post:
        raise HTTPException(status_code=404, detail="Post not found")
    return post


@router.put("/{id}", response_model=PostResponse)
async def update_post(
    id: int,
    post_data: PostBase,
    session: SessionDep,
    current_id: Annotated[TokenData, Depends(oauth2.get_current_user)],
):
    post = session.query(models.DBPost).filter(models.DBPost.id == id).first()
    if not post:
        raise HTTPException(status_code=404, detail="Post not found")

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
    current_id: Annotated[TokenData, Depends(oauth2.get_current_user)],
):
    post = session.query(models.DBPost).filter(models.DBPost.id == id).first()
    if not post:
        raise HTTPException(status_code=404, detail="Post not found")

    session.delete(post)
    session.commit()
    return Response(status_code=204)
