from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from database import get_db
from models import DBUser, DBSwipe

from base import BaseAPI

from pydantic import BaseModel


class UserCreate(BaseModel):
    name: str




class UserResponse(BaseModel):
    id: int
    name: str

    class Config:
        from_attributes = True


class UserSwipeResponse(BaseModel):
    id: int
    user_id: int
    movie_id: int
    swipe_type: str

    class Config:
        from_attributes = True


router = APIRouter(
    prefix="/users",
    tags=["Users"]
)

base_api = BaseAPI()


@router.post("/", response_model=UserResponse)
def create_user(user: UserCreate, db: Session = Depends(get_db)):
    new_user = DBUser(name=user.name)

    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return new_user


@router.get("/", response_model=list[UserResponse])
def get_all_users(db: Session = Depends(get_db)):
    return db.query(DBUser).all()


@router.get("/{user_id}", response_model=UserResponse)
def get_user(user_id: int, db: Session = Depends(get_db)):
    return base_api.get_or_404(db, DBUser, user_id)

@router.delete("/{user_id}")
def delete_user(user_id: int, db: Session = Depends(get_db)):
    db_user = base_api.get_or_404(db, DBUser, user_id)

    db.delete(db_user)
    db.commit()

    return {"message": "User wurde gelöscht"}


@router.get("/{user_id}/swipes", response_model=list[UserSwipeResponse])
def get_user_swipes(user_id: int, db: Session = Depends(get_db)):
    base_api.get_or_404(db, DBUser, user_id)

    swipes = db.query(DBSwipe).filter(DBSwipe.user_id == user_id).all()

    return swipes


@router.get("/{user_id}/watched", response_model=list[UserSwipeResponse])
def get_user_watched_movies(user_id: int, db: Session = Depends(get_db)):
    base_api.get_or_404(db, DBUser, user_id)

    watched = db.query(DBSwipe).filter(DBSwipe.user_id == user_id).all()

    return watched