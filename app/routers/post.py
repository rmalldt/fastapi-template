from fastapi import HTTPException, Response, status, APIRouter
from ..schemas import PostResponse, PostBase
from .. import models
from ..database import SessionDep


router = APIRouter(prefix="/posts")


@router.get("/", response_model=list[PostResponse])
async def get_posts(session: SessionDep):
    posts = session.query(models.DBPost).all()
    if not posts:
        raise HTTPException(status_code=404, detail="No posts found")
    return posts


@router.post("/", status_code=status.HTTP_201_CREATED)
async def create_posts(post_data: PostBase, session: SessionDep):
    new_post = models.DBPost(**post_data.model_dump())
    session.add(new_post)
    session.commit()
    session.refresh(new_post)
    return new_post


@router.get("/{id}", response_model=PostResponse)
async def get_post(id: int, session: SessionDep):
    post = session.query(models.DBPost).filter(models.DBPost.id == id).first()
    if not post:
        raise HTTPException(status_code=404, detail="Post not found")
    return post


@router.put("/{id}", response_model=PostResponse)
async def update_post(id: int, post_data: PostBase, session: SessionDep):
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
async def delete_post(id: int, session: SessionDep):
    post = session.query(models.DBPost).filter(models.DBPost.id == id).first()
    if not post:
        raise HTTPException(status_code=404, detail="Post not found")

    session.delete(post)
    session.commit()
    return Response(status_code=204)
