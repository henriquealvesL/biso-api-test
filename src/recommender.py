from sqlalchemy.orm import Session
from src import models

def recommend_movies(user_id: int, db: Session):
    ratings = db.query(models.Rating).filter(models.Rating.user_id == user_id).all()
    if not ratings:
        return []
    
    watched_movie_ids = {r.movie_id for r in ratings}
    
    liked_movie_ids = {r.movie_id for r in ratings if r.score >= 4}
    
    liked_movies = db.query(models.Movie).filter(models.Movie.id.in_(liked_movie_ids)).all()
    
    favorite_genres = set(movie.genre for movie in liked_movies if movie.genre)
    favorite_directors = set(movie.director for movie in liked_movies if movie.director)
    
    candidate_movies = db.query(models.Movie).filter(~models.Movie.id.in_(watched_movie_ids)).all()

    recommendations = []
    for movie in candidate_movies:
        score = 0
        if movie.genre in favorite_genres:
            score += 2
        if movie.director in favorite_directors:
            score += 3

        if score > 0:
            recommendations.append((movie, score))
    
    recommendations.sort(key=lambda x: x[1], reverse=True)    
    return [movie for movie, _ in recommendations]
