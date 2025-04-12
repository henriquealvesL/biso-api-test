from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from src.crud import movies, ratings
from src.database import get_session
from http import HTTPStatus
from src import schemas

router = APIRouter(
  prefix="/filmes",
  tags=["filmes"]
)

@router.post("/", response_model=schemas.MovieOut, status_code=HTTPStatus.CREATED)
def create_movie(movie: schemas.MovieBase, db: Session = Depends(get_session)):
  try:
     return movies.create_movie(db, movie)
  except ValueError as e:
    raise HTTPException(status_code=404, detail=str(e))
  
@router.put("/{movie_id}", response_model=schemas.MovieBase)
def update_movie(movie_id: int, movie_update: schemas.MovieBase, db: Session = Depends(get_session)):
  try:
    updated_movie = movies.update_movie(db, movie_id, movie_update)
  except ValueError as e:
    raise HTTPException(status_code=HTTPStatus.BAD_REQUEST, detail=str(e))

  if not updated_movie:
    raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail="Movie not found")
  
  return updated_movie

@router.delete("/{movie_id}", status_code=HTTPStatus.NO_CONTENT)
def delete_movie(movie_id: int, db: Session = Depends(get_session)):
  success = movies.delete_movie(db, movie_id)
  if not success:
    raise HTTPException(status_code=404, detail="Movie not found")


@router.get("/{movie_id}", response_model=schemas.MovieOut)
def read_movie(movie_id: int, db: Session = Depends(get_session)):
  db_movie = movies.get_movie(db, movie_id=movie_id)
  if db_movie is None:
    raise HTTPException(status_code=404, detail="Movie not found")
  return db_movie

@router.get("/", response_model=schemas.MovieList, status_code=HTTPStatus.OK)
def read_movies(db: Session = Depends(get_session)):
  movies_db = movies.get_movies(db)
  return {"movies": movies_db}

@router.get("/{movie_id}/ratings", response_model=list[schemas.RatingSchema])
def get_ratings_by_movie(movie_id: int, db: Session = Depends(get_session)):
    return ratings.get_ratings_by_movie(db, movie_id)
