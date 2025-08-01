from fastapi import FastAPI

from . import models
from .database import engine
from .routers import auth, user, post, vote
from fastapi.middleware.cors import CORSMiddleware


# Now the migration is managed with Alembic
# models.Base.metadata.create_all(bind=engine)

app = FastAPI()


origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
async def root():
    return {"message": "A CRUD API template built with FastAPI"}


app.include_router(auth.router)
app.include_router(user.router)
app.include_router(post.router)
app.include_router(vote.router)
