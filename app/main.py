from fastapi import FastAPI

from . import models
from .database import engine
from .routers import auth, user, post


# Create Database tables
models.Base.metadata.create_all(bind=engine)

# FastAPI app
app = FastAPI()

app.include_router(auth.router)
app.include_router(user.router)
app.include_router(post.router)
