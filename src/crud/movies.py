from sqlalchemy.orm import Session
from sqlalchemy import func
from src import models, schemas

def create_movie(db: Session, movie: schemas.MovieBase):
  if db.query(models.Movie).filter(func.lower(models.Movie.title) == movie.title.lower()).first():
    raise ValueError(f"Movie with title '{movie.title}' already exists")
  
  db_movie = models.Movie(
    title=movie.title,
    genre=movie.genre,
    director=movie.director
  )
  db.add(db_movie)
  db.commit()
  db.refresh(db_movie)
  return db_movie

def update_movie(db: Session, movie_id: int, movie_update: schemas.MovieBase):
    db_movie = db.query(models.Movie).filter(models.Movie.id == movie_id).first()
    if not db_movie:
        return None
    
    existing_movie = (
        db.query(models.Movie)
        .filter(func.lower(models.Movie.title) == movie_update.title.lower())
        .filter(models.Movie.id != movie_id)
        .first()
    )
    if existing_movie:
        raise ValueError(f"Movie with title '{movie_update.title}' already exists")

    db_movie.title = movie_update.title
    db_movie.genre = movie_update.genre
    db_movie.director = movie_update.director
    
    db.commit()
    db.refresh(db_movie)
    return db_movie

def delete_movie(db: Session, movie_id: int):
    db_movie = db.query(models.Movie).filter(models.Movie.id == movie_id).first()
    if not db_movie:
        return None

    db.delete(db_movie)
    db.commit()
    return db_movie

def get_movie(db: Session, movie_id: int):
  return db.query(models.Movie).filter(models.Movie.id == movie_id).first()

def get_movies(db: Session, skip: int = 0, limit: int = 100):
  return db.query(models.Movie).offset(skip).limit(limit).all()
