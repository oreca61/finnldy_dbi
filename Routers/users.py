from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from pydantic import BaseModel, Field

from database import get_db
from models import DBUser, DBSwipe
from Routers.base import BaseAPI
from auth import get_current_role, require_admin
from logger_config import logger


class UserCreate(BaseModel):
    name: str = Field(min_length=2, max_length=20)


class UserUpdate(BaseModel):
    name: str = Field(min_length=2, max_length=20)


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


@router.post("/", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
def create_user(
    user: UserCreate,
    db: Session = Depends(get_db),
    role: str = Depends(get_current_role)
):
    require_admin(role)

    logger.info("POST /users aufgerufen")

    new_user = DBUser(name=user.name)

    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    logger.info("User mit ID %s wurde erstellt", new_user.id)

    return new_user


@router.get("/", response_model=list[UserResponse])
def get_all_users(
    db: Session = Depends(get_db),
    role: str = Depends(get_current_role)
):
    logger.info("GET /users aufgerufen")
    return db.query(DBUser).all()


@router.get("/{user_id}", response_model=UserResponse)
def get_user(
    user_id: int,
    db: Session = Depends(get_db),
    role: str = Depends(get_current_role)
):
    logger.info("GET /users/%s aufgerufen", user_id)
    return base_api.get_or_404(db, DBUser, user_id)


@router.put("/{user_id}", response_model=UserResponse)
def update_user(
    user_id: int,
    user: UserUpdate,
    db: Session = Depends(get_db),
    role: str = Depends(get_current_role)
):
    require_admin(role)

    logger.info("PUT /users/%s aufgerufen", user_id)

    db_user = base_api.get_or_404(db, DBUser, user_id)
    db_user.name = user.name

    db.commit()
    db.refresh(db_user)

    logger.info("User mit ID %s wurde aktualisiert", user_id)

    return db_user


@router.delete("/{user_id}")
def delete_user(
    user_id: int,
    db: Session = Depends(get_db),
    role: str = Depends(get_current_role)
):
    require_admin(role)

    logger.info("DELETE /users/%s aufgerufen", user_id)

    db_user = base_api.get_or_404(db, DBUser, user_id)

    db.delete(db_user)
    db.commit()

    logger.info("User mit ID %s wurde gelöscht", user_id)

    return {
        "message": "User wurde gelöscht",
        "id": user_id
    }


@router.get("/{user_id}/swipes", response_model=list[UserSwipeResponse])
def get_user_swipes(
    user_id: int,
    db: Session = Depends(get_db),
    role: str = Depends(get_current_role)
):
    logger.info("GET /users/%s/swipes aufgerufen", user_id)

    base_api.get_or_404(db, DBUser, user_id)

    swipes = db.query(DBSwipe).filter(DBSwipe.user_id == user_id).all()

    return swipes