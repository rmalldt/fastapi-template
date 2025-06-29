import os
import time
from fastapi import FastAPI, HTTPException, Response, status, Depends
from pydantic import BaseModel
import uvicorn
from dotenv import load_dotenv
import psycopg2
from psycopg2.extras import RealDictCursor
from sqlalchemy.orm import Session
import models
from database import engine, get_db

models.Base.metadata.create_all(bind=engine)
load_dotenv()
app = FastAPI()


class Post(BaseModel):
    title: str
    content: str
    published: bool = True


while True:
    try:
        conn = psycopg2.connect(
            host=os.getenv("DB_HOST"),
            database=os.getenv("DB_NAME"),
            user=os.getenv("DB_USER"),
            password=os.getenv("DB_PASSWORD"),
            cursor_factory=RealDictCursor,
        )
        cursor = conn.cursor()
        print(f"Database connection successful.")
        break
    except Exception as error:
        print(f"Failed to connect database. Error: {error}")
        time.sleep(2)


@app.get("/sqlalchemy")
def get_session(db: Session = Depends(get_db)):
    return {"status": "Success"}


@app.get("/")
async def root():
    return {"message": "A CRUD API for testing."}


@app.get("/posts")
async def get_posts():
    cursor.execute("""SELECT * FROM post LIMIT 100;""")
    posts = cursor.fetchall()
    return {"success": True, "data": posts}


# POST /posts
@app.post("/posts")
async def create_posts(post: Post, response: Response):
    cursor.execute(
        """INSERT INTO post (title, content) VALUES (%s, %s) RETURNING *;""",
        (post.title, post.content),
    )
    new_post = cursor.fetchone()
    conn.commit()  # finalize and push the changes to the DB
    response.status_code = status.HTTP_201_CREATED
    return {"success": True, "data": new_post}


@app.get("/posts/{id}")
async def get_post(id: int):
    cursor.execute("""SELECT * FROM post WHERE id = %s;""", (str(id),))
    post = cursor.fetchone()
    if not post:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Post with id: {id} not found",
        )
    return {"success": True, "data": post}


@app.delete("/posts/{id}")
async def delete_post(id: int):
    cursor.execute("""DELETE FROM post WHERE id = %s RETURNING *;""", (str(id),))
    deleted_post = cursor.fetchone()
    conn.commit()
    if not deleted_post:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Post with id: {id} not found",
        )
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@app.put("/posts/{id}")
async def update_post(id: int, post: Post):
    cursor.execute(
        """UPDATE post SET title = %s, content = %s WHERE id = %s RETURNING *;""",
        (post.title, post.content, str(id)),
    )
    updated_post = cursor.fetchone()
    conn.commit()
    if not updated_post:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Post with id: {id} not found",
        )
    return {"result": True, "data": updated_post}


if __name__ == "__main__":
    uvicorn.run(app="main:app", host="127.0.0.1", port=8000, reload=True)
