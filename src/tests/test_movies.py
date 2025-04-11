
def test_create_movie(client):
    response = client.post("/filmes/", json={
        "title": "Inception",
        "genre": "Sci-Fi",
        "director": "Christopher Nolan"
    })
    assert response.status_code == 201
    data = response.json()
    assert data["title"] == "Inception"

def test_get_movie(client):
    response = client.get("/filmes/1")
    assert response.status_code == 200
    data = response.json()
    assert data["title"] == "Inception"

def test_update_movie(client):
    response = client.put("/filmes/1", json={
        "title": "Inception Updated",
        "genre": "Action",
        "director": "Nolan"
    })
    assert response.status_code == 200
    data = response.json()
    assert data["title"] == "Inception Updated"

def test_create_duplicate_movie(client):
    response = client.post("/filmes/", json={
        "title": "Inception Updated",
        "genre": "Sci-Fi",
        "director": "Someone Else"
    })
    assert response.status_code == 404
    assert "already exists" in response.json()["detail"]

def test_get_all_movies(client):
    response = client.get("/filmes/")
    assert response.status_code == 200
    assert isinstance(response.json()["movies"], list)

def test_delete_movie(client):
    response = client.delete("/filmes/1")
    assert response.status_code == 204

    response = client.get("/filmes/1")
    assert response.status_code == 404
