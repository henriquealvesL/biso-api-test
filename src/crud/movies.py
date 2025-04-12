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

def bulk_create_movies(db: Session, batch: schemas.MovieBatch):
    req_titles = [movie.title.lower() for movie in batch.movies]
    
    duplicate_movies = db.query(models.Movie)\
        .filter(func.lower(models.Movie.title).in_(req_titles))\
        .all()
    
    if duplicate_movies:
      duplicate_titles = [movie.title for movie in duplicate_movies]
      raise ValueError(f"The following movies already exist: {', '.join(duplicate_titles)}")
    
    movies_data = [movie.model_dump() for movie in batch.movies]
    db.bulk_insert_mappings(models.Movie, movies_data)
    db.commit()
    
    return movies_data

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
