from sqlalchemy.orm import Session
from sqlalchemy import func
from src import models, schemas

def create_user(db: Session, user: schemas.UserSchema):
  if db.query(models.User).filter(func.lower(models.User.name) == user.name.lower()).first():
    raise ValueError(f"User with name '{user.name}' already exists")
  
  db_user = models.User(name=user.name)
  db.add(db_user)
  db.commit()
  db.refresh(db_user)
  return db_user

def update_user(db: Session, user_id: int, user_update: schemas.UserSchema):
    db_user = db.query(models.User).filter(models.User.id == user_id).first()
    if not db_user:
        return None
    
    existing_user = (
        db.query(models.User)
        .filter(func.lower(models.User.name) == user_update.name.lower())
        .filter(models.User.id != user_id)
        .first()
    )
    if existing_user:
        raise ValueError(f"User with name '{user_update.name}' already exists")

    db_user.name = user_update.name
    db.commit()
    db.refresh(db_user)
    return db_user

def delete_user(db: Session, user_id: int):
    db_user = db.query(models.User).filter(models.User.id == user_id).first()
    if not db_user:
        return None

    db.delete(db_user)
    db.commit()
    return db_user

def get_user(db: Session, user_id: int):
  return db.query(models.User).filter(models.User.id == user_id).first()

def get_users(db: Session, skip: int = 0, limit: int = 100):
  return db.query(models.User).offset(skip).limit(limit).all()
