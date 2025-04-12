from sqlalchemy.orm import Session
from src import models, schemas

def create_rating(db: Session, rating: schemas.RatingSchema):
    user = db.query(models.User).filter(models.User.id == rating.user_id).first()

    if not user:
        raise ValueError(f"User with id '{rating.user_id}' not found")

    movie = db.query(models.Movie).filter(models.Movie.id == rating.movie_id).first()
    if not movie:
        raise ValueError(f"Movie with id '{rating.movie_id}' not found")


    db_rating = models.Rating(
        user_id=rating.user_id,
        movie_id=rating.movie_id,
        score=rating.score
    )
    db.add(db_rating)
    db.commit()
    db.refresh(db_rating)

    return db_rating

def get_all_ratings(db: Session):
    return db.query(models.Rating).all()


def get_ratings_by_movie(db: Session, movie_id: int):
    return db.query(models.Rating).filter(models.Rating.movie_id == movie_id).all()


def get_ratings_by_user(db: Session, user_id: int):
    return db.query(models.Rating).filter(models.Rating.user_id == user_id).all()
