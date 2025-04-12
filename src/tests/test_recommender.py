from http import HTTPStatus

def test_recommendations_user_not_found(client):
    response = client.get("/filmes/9999/recomendacoes")
    assert response.status_code == HTTPStatus.NOT_FOUND
    assert response.json()["detail"] == "User not found"

def test_recommendations_empty(client):
    user_response = client.post("/users/", json={"name": "TestUser"})
    user = user_response.json()
    user_id = user["id"]

    response = client.get(f"/filmes/{user_id}/recomendacoes")
    assert response.status_code == HTTPStatus.OK

    data = response.json()
    assert "movies" in data
    assert isinstance(data["movies"], list)
    assert len(data["movies"]) == 0


def test_recommendations_with_ratings(client):
    user_response = client.post("/users/", json={"name": "RecomUser"})
    user = user_response.json()
    user_id = user["id"]

    movie1 = client.post("/filmes/", json={
        "title": "Fav Movie 1",
        "genre": "Action",
        "director": "Dir A"
    }).json()
    movie2 = client.post("/filmes/", json={
        "title": "Fav Movie 2",
        "genre": "Comedy",
        "director": "Dir B"
    }).json()

    client.post("/ratings/", json={
        "user_id": user_id,
        "movie_id": movie1["id"],
        "score": 5
    })
    client.post("/ratings/", json={
        "user_id": user_id,
        "movie_id": movie2["id"],
        "score": 4
    })

    #Should be recommended
    candidate1 = client.post("/filmes/", json={
        "title": "Candidate 1",
        "genre": "Action",
        "director": "Dir X"
    }).json()

    #Should be recommended
    candidate2 = client.post("/filmes/", json={
        "title": "Candidate 2",
        "genre": "Drama",
        "director": "Dir A"
    }).json()

    # Don't should be recommended
    candidate3 = client.post("/filmes/", json={
        "title": "Candidate 3",
        "genre": "Horror",
        "director": "Dir Z"
    }).json()

    response = client.get(f"/filmes/{user_id}/recomendacoes")
    assert response.status_code == HTTPStatus.OK
    data = response.json()
    assert "movies" in data
    recommendations = data["movies"]
    
    rec_ids = {movie["id"] for movie in recommendations}

    assert candidate1["id"] in rec_ids
    assert candidate2["id"] in rec_ids
    assert candidate3["id"] not in rec_ids
