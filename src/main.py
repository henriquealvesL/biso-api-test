from fastapi import FastAPI

app = FastAPI()


@app.get("/filmes")
def read_movies():
    return ["Avengers", "Now you see me"]
