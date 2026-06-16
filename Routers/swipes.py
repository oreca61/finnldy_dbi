from typing import Literal

from fastapi import APIRouter, Depends, status
from pydantic import BaseModel, Field
from sqlalchemy.orm import Session
from sqlalchemy import func, case

from database import get_db
from models import DBUser, DBMovies, DBSwipe
from auth import get_current_role, require_admin
from logger_config import logger


router = APIRouter(
    prefix="/swipes",
    tags=["Swipes"]
)


class SwipeCreate(BaseModel):
    username: str = Field(min_length=2, max_length=20)
    api_movie_id: int = Field(gt=0)
    movie_title: str = Field(min_length=1, max_length=50)
    swipe_type: Literal["Like", "Dislike", "Watched", "WatchLater"]


class SwipeResponse(BaseModel):
    id: int
    user_id: int
    movie_id: int
    swipe_type: str

    class Config:
        from_attributes = True


class ResultResponse(BaseModel):
    movie_id: int
    api_movie_id: int
    title: str
    likes: int
    dislikes: int
    watched: int
    watch_later: int
    score: int


@router.post("/", response_model=SwipeResponse, status_code=status.HTTP_201_CREATED)
def create_swipe(
    swipe: SwipeCreate,
    db: Session = Depends(get_db),
    role: str = Depends(get_current_role)
):
    require_admin(role)

    logger.info("POST /swipes aufgerufen")

    # User suchen oder erstellen
    user = db.query(DBUser).filter(DBUser.name == swipe.username).first()

    if user is None:
        user = DBUser(name=swipe.username)
        db.add(user)
        db.commit()
        db.refresh(user)

    # Film suchen oder erstellen
    movie = db.query(DBMovies).filter(DBMovies.api_movie_id == swipe.api_movie_id).first()

    if movie is None:
        movie = DBMovies(
            api_movie_id=swipe.api_movie_id,
            title=swipe.movie_title[:50],
            description=None,
            release_date=None
        )

        db.add(movie)
        db.commit()
        db.refresh(movie)

    # Swipe speichern
    new_swipe = DBSwipe(
        user_id=user.id,
        movie_id=movie.id,
        swipe_type=swipe.swipe_type
    )

    db.add(new_swipe)
    db.commit()
    db.refresh(new_swipe)

    logger.info(
        "Swipe gespeichert: User %s, Film %s, Typ %s",
        user.name,
        movie.title,
        swipe.swipe_type
    )

    return new_swipe


@router.get("/results", response_model=list[ResultResponse])
def get_results(
    db: Session = Depends(get_db),
    role: str = Depends(get_current_role)
):
    logger.info("GET /swipes/results aufgerufen")

    likes = func.sum(
        case((DBSwipe.swipe_type == "Like", 1), else_=0)
    ).label("likes")

    dislikes = func.sum(
        case((DBSwipe.swipe_type == "Dislike", 1), else_=0)
    ).label("dislikes")

    watched = func.sum(
        case((DBSwipe.swipe_type == "Watched", 1), else_=0)
    ).label("watched")

    watch_later = func.sum(
        case((DBSwipe.swipe_type == "WatchLater", 1), else_=0)
    ).label("watch_later")

    score = (
        func.sum(case((DBSwipe.swipe_type == "Like", 3), else_=0)) +
        func.sum(case((DBSwipe.swipe_type == "WatchLater", 1), else_=0)) -
        func.sum(case((DBSwipe.swipe_type == "Dislike", 1), else_=0)) -
        func.sum(case((DBSwipe.swipe_type == "Watched", 2), else_=0))
    ).label("score")

    results = (
        db.query(
            DBMovies.id.label("movie_id"),
            DBMovies.api_movie_id.label("api_movie_id"),
            DBMovies.title.label("title"),
            likes,
            dislikes,
            watched,
            watch_later,
            score
        )
        .join(DBSwipe, DBSwipe.movie_id == DBMovies.id)
        .group_by(DBMovies.id)
        .order_by(score.desc())
        .limit(5)
        .all()
    )

    return results