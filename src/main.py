from fastapi import FastAPI
from src.routers import users, movies

app = FastAPI()

app.include_router(users.router)
app.include_router(movies.router)