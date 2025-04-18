from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from src.crud import users, ratings
from src.database import get_session
from http import HTTPStatus
from src import schemas

router = APIRouter(
    prefix="/users",
    tags=["users"]
)

@router.post("/", response_model=schemas.UserOut, status_code=HTTPStatus.CREATED)
def create_user(user: schemas.UserBase, db: Session = Depends(get_session)):
    try:
       return users.create_user(db, user)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    
@router.put("/{user_id}", response_model=schemas.UserBase)
def update_user(user_id: int, user_update: schemas.UserBase, db: Session = Depends(get_session)):
    try:
        updated_user = users.update_user(db, user_id, user_update)
    except ValueError as e:
        raise HTTPException(status_code=HTTPStatus.BAD_REQUEST, detail=str(e))

    if not updated_user:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail="User not found")
    
    return updated_user

@router.delete("/{user_id}", status_code=HTTPStatus.NO_CONTENT)
def delete_user(user_id: int, db: Session = Depends(get_session)):
    success = users.delete_user(db, user_id)
    if not success:
        raise HTTPException(status_code=404, detail="User not found")


@router.get("/{user_id}", response_model=schemas.UserOut)
def read_user(user_id: int, db: Session = Depends(get_session)):
    db_user = users.read_user(db, user_id=user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user

@router.get("/", response_model=schemas.UserList, status_code=HTTPStatus.OK)
def read_users(db: Session = Depends(get_session)):
    users_db = users.read_users(db)
    return {"users": users_db}


@router.get("/{user_id}/ratings", response_model=list[schemas.RatingSchema])
def get_ratings_by_user(user_id: int, db: Session = Depends(get_session)):
    return ratings.get_ratings_by_user(db, user_id)
