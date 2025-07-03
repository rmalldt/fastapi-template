from fastapi import FastAPI

from . import models
from .database import engine
from .routers import auth, user, post


models.Base.metadata.create_all(bind=engine)

app = FastAPI()


@app.get("/")
async def root():
    return {"message": "A CRUD API template built with FastAPI"}


app.include_router(auth.router)
app.include_router(user.router)
app.include_router(post.router)
