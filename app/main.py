from random import randrange
from typing import Optional
from fastapi import FastAPI, HTTPException, Response, status
from pydantic import BaseModel
import uvicorn

# FastAPI ASGI app
app = FastAPI()


# Class using pydantic BaseModel
class Post(BaseModel):
    title: str
    content: str
    published: bool = True
    rating: Optional[int] = None


# Mock DB
db_posts = [
    {
        "title": "Post 1",
        "content": "Content of the post 1 ",
        "rating": 5,
        "id": 1,
    },
    {
        "title": "Post 2",
        "content": "Content of the post 2",
        "rating": 3,
        "id": 2,
    },
]


# Find Post
def find_post(id: int) -> dict | None:
    for post in db_posts:
        if post["id"] == id:
            return post


# Find Post, same as above but using generator
def find_post_gen(id: int):
    res = next((post for post in db_posts if post["id"] == id), None)
    return res


# Find Post index
def find_post_index(id: int) -> int | None:
    for i, post in enumerate(db_posts):
        if post["id"] == id:
            return i


# GET /
@app.get("/")
async def root():
    # FastAPI automatically converts the Python dict to json
    return {"message": "Hello there!"}


# GET /posts
@app.get("/posts")
async def get_posts():
    # FastAPI automatically converts the Python array to json
    return {"data": db_posts}


# POST /posts
@app.post("/posts")
async def create_posts(post: Post, response: Response):
    post_dict = post.model_dump()
    post_dict["id"] = randrange(1, 1000)
    db_posts.append(post_dict)
    response.status_code = status.HTTP_201_CREATED
    return {"data": post_dict}


# GET /posts/:id
# Note: The extracted param values are always String type.
# Always annotate the function param type and FastAPI will
# automatically validate (check that type can be converted)
# and parse the received type into the requried to type.
# E.g., str is converted to int below.
@app.get("/posts/{id}")
async def get_post(id: int):
    post = find_post_gen(id)
    if not post:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"post with id: {id} not found",
        )
    return {"data": post}


# DELETE /posts
@app.delete("/posts/{id}")
async def delete_post(id: int):
    index = find_post_index(id)
    if index == None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"post with id: {id} not found",
        )
    db_posts.pop(index)

    # Send only status code as response.
    # Delete request doesn't require response data to be sent.
    return Response(status_code=status.HTTP_204_NO_CONTENT)


# PUT /posts/:id
@app.put("/posts/{id}")
async def update_post(id: int, post: Post):
    index = find_post_index(id)
    if index == None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"post with id: {id} not found",
        )
    post_dict = post.model_dump()
    post_dict["id"] = id
    db_posts[index] = post_dict
    return {"data": post_dict}


if __name__ == "__main__":
    uvicorn.run(app="main:app", host="127.0.0.1", port=8000, reload=True)
