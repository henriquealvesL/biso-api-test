from pydantic import BaseModel, Field
from typing import Optional

class UserBase(BaseModel):
  name: str

class UserOut(UserBase):
  id: int
class UserList(BaseModel):
  users: list[UserOut]

class MovieBase(BaseModel):
  title: str
  genre: str
  director: Optional[str]

class MovieOut(MovieBase):
  id: int

class MovieList(BaseModel):
  movies: list[MovieOut]

class RatingSchema(BaseModel):
  user_id: int
  movie_id: int
  score: int = Field(..., ge=1, le=5)