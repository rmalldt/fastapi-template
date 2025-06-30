from fastapi import FastAPI, HTTPException, Response, status, Depends
import uvicorn
from dotenv import load_dotenv
from sqlalchemy.orm import Session
import models
from schemas import Post
from database import engine, get_db

models.Base.metadata.create_all(bind=engine)
load_dotenv()
app = FastAPI()


@app.get("/")
async def root():
    return {"message": "A CRUD API for testing."}


@app.get("/posts")
async def get_posts(db: Session = Depends(get_db)):
    posts = db.query(models.Post).all()
    if not posts:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"No posts found",
        )
    return {"success": True, "data": posts}


@app.post("/posts")
async def create_posts(post: Post, response: Response, db: Session = Depends(get_db)):
    new_post = models.Post(**post.model_dump())
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    response.status_code = status.HTTP_201_CREATED
    return {"success": True, "data": new_post}


@app.get("/posts/{id}")
async def get_post(id: int, db: Session = Depends(get_db)):
    post = db.query(models.Post).filter(models.Post.id == id).first()
    if not post:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Post with id: {id} not found",
        )
    return {"success": True, "data": post}


@app.delete("/posts/{id}")
async def delete_post(id: int, db: Session = Depends(get_db)):
    post_query = db.query(models.Post).filter(models.Post.id == id)
    if post_query.first() == None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Post with id: {id} not found",
        )
    post_query.delete(synchronize_session=False)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@app.put("/posts/{id}")
async def update_post(id: int, post: Post, db: Session = Depends(get_db)):
    post_query = db.query(models.Post).filter(models.Post.id == id)
    if post_query.first() == None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Post with id: {id} not found",
        )
    post_query.update(post.model_dump(), synchronize_session=False)
    db.commit()
    return {"result": True, "data": post_query.first()}


if __name__ == "__main__":
    uvicorn.run(app="main:app", host="127.0.0.1", port=8000, reload=True)
