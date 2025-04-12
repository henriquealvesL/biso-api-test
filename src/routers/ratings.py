from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from src import schemas
from src.crud import ratings
from src.database import get_session

router = APIRouter(
    prefix="/ratings",
    tags=["ratings"]
)

@router.post("/", response_model=schemas.RatingSchema, status_code=status.HTTP_201_CREATED)
def rate_movie(rating: schemas.RatingSchema, db: Session = Depends(get_session)):
    try:
        new_rating = ratings.create_rating(db, rating)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

    return new_rating

@router.get("/", response_model=list[schemas.RatingSchema])
def get_all_ratings(db: Session = Depends(get_session)):
    return ratings.get_all_ratings(db)
