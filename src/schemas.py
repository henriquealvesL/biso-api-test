from pydantic import BaseModel, Field
from typing import Optional

class UserSchema(BaseModel):
  name: str

class UserList(BaseModel):
  users: list[UserSchema]

class MovieSchema(BaseModel):
  title: str
  description: str
  genre: str
  director: Optional[str]

class RatingSchema(BaseModel):
  user_id: int
  movie_id: int
  score: int = Field(..., ge=1, le=5)