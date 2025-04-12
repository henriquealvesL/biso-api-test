from http import HTTPStatus

def test_create_rating(client):
    user = client.post("/users/", json={"name": "John"}).json()
    movie = client.post("/filmes/", json={"title": "Matrix", "genre": "Sci-Fi", "director": "Wachowski"}).json()

    response = client.post("/ratings/", json={
        "user_id": user["id"],
        "movie_id": movie["id"],
        "score": 4
    })

    assert response.status_code == HTTPStatus.CREATED
    assert response.json()["score"] == 4

def test_get_all_ratings(client):
    user = client.post("/users/", json={"name": "Max"}).json()
    movie1 = client.post("/filmes/", json={"title": "Movie1", "genre": "Drama", "director": "A"}).json()
    movie2 = client.post("/filmes/", json={"title": "Movie2", "genre": "Action", "director": "B"}).json()

    client.post("/ratings/", json={"user_id": user["id"], "movie_id": movie1["id"], "score": 3})
    client.post("/ratings/", json={"user_id": user["id"], "movie_id": movie2["id"], "score": 5})

    response = client.get("/ratings/")
    print("Response: ", response)
    assert response.status_code == HTTPStatus.OK
    assert len(response.json()) == 2

def test_get_ratings_by_movie(client):
    user = client.post("/users/", json={"name": "Luna"}).json()
    movie = client.post("/filmes/", json={"title": "Interstellar", "genre": "Sci-Fi", "director": "Nolan"}).json()
    client.post("/ratings/", json={"user_id": user["id"], "movie_id": movie["id"], "score": 5})

    response = client.get(f"/filmes/{movie['id']}/ratings")
    assert response.status_code == HTTPStatus.OK
    assert response.json()[0]["score"] == 5

def test_get_ratings_by_user(client):
    user = client.post("/users/", json={"name": "Zoe"}).json()
    movie = client.post("/filmes/", json={"title": "Titanic", "genre": "Romance", "director": "Cameron"}).json()
    client.post("/ratings/", json={"user_id": user["id"], "movie_id": movie["id"], "score": 4})

    response = client.get(f"/users/{user['id']}/ratings")
    assert response.status_code == HTTPStatus.OK
    assert response.json()[0]["movie_id"] == movie["id"]
