import uvicorn
from typing import Annotated
from fastapi import FastAPI, HTTPException, Response, status, Depends
from sqlalchemy.orm import Session
import models
from schemas import PostResponse, PostBase, UserCreate, UserResponse
from database import engine, get_session
from utils import hash

# Create Database tables
models.Base.metadata.create_all(bind=engine)

# Dependency
SessionDep = Annotated[Session, Depends(get_session)]


# FastAPI app
app = FastAPI()


# Endpoints
@app.get("/")
async def root():
    return {"message": "A CRUD API for testing."}


@app.get("/users/{id}", response_model=UserResponse)
async def get_user(id: int, session: SessionDep):
    user = session.query(models.DBUser).filter(models.DBUser.id == id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user


@app.post("/users", status_code=status.HTTP_201_CREATED)
async def create_user(user_data: UserCreate, session: SessionDep):
    user = (
        session.query(models.DBUser)
        .filter(models.DBUser.email == user_data.email)
        .first()
    )
    if user:
        raise HTTPException(status_code=400, detail="Email already exists")

    # Hash the password
    hashed_pass = hash(user_data.password)
    user_data.password = hashed_pass

    # Insert the user with hashed password to DB
    new_user = models.DBUser(**user_data.model_dump())
    session.add(new_user)
    session.commit()
    session.refresh(new_user)
    return new_user


@app.get("/posts", response_model=list[PostResponse])
async def get_posts(session: SessionDep):
    posts = session.query(models.DBPost).all()
    if not posts:
        raise HTTPException(status_code=404, detail="No posts found")
    return posts


@app.post("/posts", status_code=status.HTTP_201_CREATED)
async def create_posts(post_data: PostBase, session: SessionDep):
    new_post = models.DBPost(**post_data.model_dump())
    session.add(new_post)
    session.commit()
    session.refresh(new_post)
    return new_post


@app.get("/posts/{id}", response_model=PostResponse)
async def get_post(id: int, session: SessionDep):
    post = session.query(models.DBPost).filter(models.DBPost.id == id).first()
    if not post:
        raise HTTPException(status_code=404, detail="Post not found")
    return post


@app.put("/posts/{id}", response_model=PostResponse)
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


@app.delete("/posts/{id}")
async def delete_post(id: int, session: SessionDep):
    post = session.query(models.DBPost).filter(models.DBPost.id == id).first()
    if not post:
        raise HTTPException(status_code=404, detail="Post not found")

    session.delete(post)
    session.commit()
    return Response(status_code=204)


if __name__ == "__main__":
    uvicorn.run(app="main:app", host="127.0.0.1", port=8000, reload=True)
