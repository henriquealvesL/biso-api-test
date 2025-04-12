from fastapi import FastAPI
from src.routers import users, movies, ratings

app = FastAPI()

app.include_router(users.router)
app.include_router(movies.router)
app.include_router(ratings.router)