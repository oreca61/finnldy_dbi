
from fastapi import APIRouter, Depends, status, HTTPException, Query
from sqlalchemy.orm import Session
from pydantic import BaseModel, Field, field_validator

from database import get_db
from models import DBUser, DBSwipe
from Routers.base import BaseAPI
from auth import get_current_role, require_admin
from logger_config import logger



class UserCreate(BaseModel):
    name: str = Field(
        min_length=2,
        max_length=20,
        description="Name des Users, zwischen 2 und 20 Zeichen"
    )

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
    name: str = Field(
        min_length=2,
        max_length=20,
        description="Neuer Name des Users"
    )

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

    # SQL-INJECTION-SCHUTZ: von Ki gemacht

    existing_user = db.query(DBUser).filter(DBUser.name == user.name).first()

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

    # SQL-INJECTION-SCHUTZ: von Ki gemacht
    users = db.query(DBUser).offset(offset).limit(limit).all()

    return users



@router.get("/{user_id}", response_model=UserResponse)
def get_user(
    user_id: int,
    db: Session = Depends(get_db),
    role: str = Depends(get_current_role)
):
    logger.info("GET /users/%s aufgerufen", user_id)

    # SQL-INJECTION-SCHUTZ:
    # user_id ist int und wird durch FastAPI validiert.
    # Die Abfrage läuft über SQLAlchemy ORM.
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

    # SQL-INJECTION-SCHUTZ:
    # Auch hier wird kein SQL-String selbst gebaut.
    existing_user = db.query(DBUser).filter(DBUser.name == user.name).first()

    if existing_user and existing_user.id != user_id:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=f"Ein anderer User mit dem Namen '{user.name}' existiert bereits."
        )

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

    # SQL-INJECTION-SCHUTZ: Ki hilfe
    # user_id wird nicht in einen SQL-String eingefügt.
    # SQLAlchemy ORM macht daraus eine sichere parametrisierte Abfrage.
    swipes = db.query(DBSwipe).filter(DBSwipe.user_id == user_id).all()

    return swipes

