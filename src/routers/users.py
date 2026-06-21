#KI anfang
# gpt: hab jatzt so ein src folder kannst das bei den imports so ändern dass es auch so jetzt passt?
from fastapi import APIRouter, Depends, status, HTTPException, Query
from sqlalchemy.orm import Session
from pydantic import BaseModel, Field, field_validator

from src.database import get_db
from src.models import DBUser, DBSwipe
from src.routers.base import BaseAPI
from src.auth import get_current_role, require_admin
from src.logger_config import logger
# KI ende

class UserCreate(BaseModel):
    name: str = Field(min_length=2, max_length=20)

    @field_validator("name")
    @classmethod
    def validate_name(cls, value):
        value = value.strip()

        if len(value) < 2:
            raise ValueError("Der Name muss mindestens 2 Zeichen lang sein.")

        if not value.replace(" ", "").isalpha():
            raise ValueError("Der Name darf nur Buchstaben und Leerzeichen enthalten.")

        return value


class UserUpdate(BaseModel):
    name: str = Field(min_length=2, max_length=20)

    @field_validator("name")
    @classmethod
    def validate_name(cls, value):
        value = value.strip()

        if len(value) < 2:
            raise ValueError("Der Name muss mindestens 2 Zeichen lang sein.")

        if not value.replace(" ", "").isalpha():
            raise ValueError("Der Name darf nur Buchstaben und Leerzeichen enthalten.")

        return value


class UserResponse(BaseModel):
    id: int
    name: str

    class Config:
        from_attributes = True

# Ki anfang
# gpt: fehlt hier etwas weil eght irgedsiw nicht
class UserSwipeResponse(BaseModel):
    id: int
    user_id: int
    movie_id: int
    swipe_type: str

    class Config:
        from_attributes = True

# Ki ende

class DeleteUserResponse(BaseModel):
    message: str
    id: int


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

    existing_user = db.query(DBUser).filter(DBUser.name == user.name).first() # Singeline chat gpt: kannst du das die anschauen sollte was falsch sein glob

    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=f"User mit dem Namen '{user.name}' existiert bereits."
        )

    new_user = DBUser(name=user.name)

    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    logger.info("User mit ID %s wurde erstellt", new_user.id)

    return new_user


@router.get("/", response_model=list[UserResponse])
def get_all_users(
    db: Session = Depends(get_db),
    role: str = Depends(get_current_role),
    limit: int = Query(default=50, ge=1, le=100),
    offset: int = Query(default=0, ge=0)
):
    logger.info("GET /users aufgerufen")

    users = db.query(DBUser).offset(offset).limit(limit).all()

    return users

#Ki anfang

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

    db_user =base_api.get_or_404(db, DBUser, user_id)

    duplicate_user =(
        db.query(DBUser) .filter(DBUser.name == user.name,DBUser.id !=user_id). first()
    )

    if duplicate_user:

        raise HTTPException(
            status_code =status.HTTP_409_CONFLICT,
            detail= f"Ein anderer User mit dem Namen '{user.name}' existiert bereits."

        )



    db_user.name = user.name
    db.commit()
    db.refresh(db_user)

    logger.info("User mit ID %s wurde aktualisiert", user_id)

    return db_user


@router.delete("/{user_id}",response_model=DeleteUserResponse, status_code=status.HTTP_200_OK )

def delete_user(
    user_id: int,
    db: Session = Depends(get_db),
    role: str= Depends(get_current_role)

):

    require_admin(role)

    db_user = base_api.get_or_404(db,DBUser,user_id)



    logger.info("DELETE /users/%s aufgerufen", user_id)



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