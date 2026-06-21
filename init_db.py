# KI-Anfang
# KI: ChatGPT
# prompt: Erstelle eine init_db.py für ein FastAPI-SQLAlchemy-Projekt, die Tabellen erstellt und Demo-Daten einfügt.

from datetime import date
from decimal import Decimal

from src.database import engine, SessionLocal
from src.models import (
    Base,
    DBUser,
    DBMovies,
    DBSwipe,
    DBGenre,
    DBMovieGenre,
    DBMovieDetails
)


def init_db():
    """
    Erstellt die Datenbank neu und fügt Demo-Daten ein.
    Achtung: Vorhandene Tabellen und Daten werden gelöscht.
    """

    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)

    db = SessionLocal()

    try:
        # Benutzer
        users = [
            DBUser(name="Sinem"),
            DBUser(name="Jakob"),
            DBUser(name="Anna"),
            DBUser(name="Lukas")
        ]

        db.add_all(users)
        db.commit()

        for user in users:
            db.refresh(user)

        # Filme
        movies = [
            DBMovies(
                api_movie_id=101,
                title="Inception",
                description="Ein Science-Fiction-Film über Träume und Realität.",
                release_date=date(2010, 7, 16)
            ),
            DBMovies(
                api_movie_id=102,
                title="Interstellar",
                description="Ein Film über Raumfahrt, Zeit und Familie.",
                release_date=date(2014, 11, 7)
            ),
            DBMovies(
                api_movie_id=103,
                title="Shrek",
                description="Ein Animationsfilm über einen Oger und seine Freunde.",
                release_date=date(2001, 5, 18)
            ),
            DBMovies(
                api_movie_id=104,
                title="The Dark Knight",
                description="Ein Actionfilm über Batman und den Joker.",
                release_date=date(2008, 7, 18)
            ),
            DBMovies(
                api_movie_id=105,
                title="Titanic",
                description="Ein Drama über die Titanic und eine Liebesgeschichte.",
                release_date=date(1997, 12, 19)
            )
        ]

        db.add_all(movies)
        db.commit()

        for movie in movies:
            db.refresh(movie)

        # Genres
        genres = [
            DBGenre(genre="Science Fiction"),
            DBGenre(genre="Action"),
            DBGenre(genre="Animation"),
            DBGenre(genre="Drama"),
            DBGenre(genre="Romance")
        ]

        db.add_all(genres)
        db.commit()

        for genre in genres:
            db.refresh(genre)

        # m:n Beziehung zwischen Filmen und Genres
        movie_genres = [
            DBMovieGenre(movie_id=movies[0].id, genre_id=genres[0].id),
            DBMovieGenre(movie_id=movies[1].id, genre_id=genres[0].id),
            DBMovieGenre(movie_id=movies[2].id, genre_id=genres[2].id),
            DBMovieGenre(movie_id=movies[3].id, genre_id=genres[1].id),
            DBMovieGenre(movie_id=movies[4].id, genre_id=genres[3].id),
            DBMovieGenre(movie_id=movies[4].id, genre_id=genres[4].id)
        ]

        db.add_all(movie_genres)

        # 1:1 Details zu Filmen
        movie_details = [
            DBMovieDetails(
                movie_id=movies[0].id,
                dauer=148,
                erlaubtes_alter=12,
                bewertung=Decimal("8.8")
            ),
            DBMovieDetails(
                movie_id=movies[1].id,
                dauer=169,
                erlaubtes_alter=12,
                bewertung=Decimal("8.7")
            ),
            DBMovieDetails(
                movie_id=movies[2].id,
                dauer=90,
                erlaubtes_alter=6,
                bewertung=Decimal("7.9")
            ),
            DBMovieDetails(
                movie_id=movies[3].id,
                dauer=152,
                erlaubtes_alter=12,
                bewertung=Decimal("9.0")
            ),
            DBMovieDetails(
                movie_id=movies[4].id,
                dauer=194,
                erlaubtes_alter=12,
                bewertung=Decimal("7.9")
            )
        ]

        db.add_all(movie_details)

        # Swipes / Bewertungen
        swipes = [
            DBSwipe(user_id=users[0].id, movie_id=movies[0].id, swipe_type="Like"),
            DBSwipe(user_id=users[1].id, movie_id=movies[0].id, swipe_type="Like"),
            DBSwipe(user_id=users[2].id, movie_id=movies[0].id, swipe_type="WatchLater"),
            DBSwipe(user_id=users[3].id, movie_id=movies[0].id, swipe_type="Dislike"),

            DBSwipe(user_id=users[0].id, movie_id=movies[1].id, swipe_type="Like"),
            DBSwipe(user_id=users[1].id, movie_id=movies[1].id, swipe_type="Like"),
            DBSwipe(user_id=users[2].id, movie_id=movies[1].id, swipe_type="Like"),
            DBSwipe(user_id=users[3].id, movie_id=movies[1].id, swipe_type="WatchLater"),

            DBSwipe(user_id=users[0].id, movie_id=movies[2].id, swipe_type="Watched"),
            DBSwipe(user_id=users[1].id, movie_id=movies[2].id, swipe_type="Like"),
            DBSwipe(user_id=users[2].id, movie_id=movies[2].id, swipe_type="Dislike"),

            DBSwipe(user_id=users[0].id, movie_id=movies[3].id, swipe_type="Like"),
            DBSwipe(user_id=users[1].id, movie_id=movies[3].id, swipe_type="WatchLater"),
            DBSwipe(user_id=users[2].id, movie_id=movies[3].id, swipe_type="Like"),
            DBSwipe(user_id=users[3].id, movie_id=movies[3].id, swipe_type="Watched"),

            DBSwipe(user_id=users[0].id, movie_id=movies[4].id, swipe_type="Dislike"),
            DBSwipe(user_id=users[1].id, movie_id=movies[4].id, swipe_type="Watched"),
            DBSwipe(user_id=users[2].id, movie_id=movies[4].id, swipe_type="WatchLater")
        ]

        db.add_all(swipes)

        db.commit()

        print("Datenbank wurde erfolgreich neu erstellt und mit Demo-Daten befüllt.")
        print("Tabellen: users, movies, swipes, genres, movie_genres, movie_details")

    except Exception as e:
        db.rollback()
        print("Fehler beim Initialisieren der Datenbank:")
        print(e)

    finally:
        db.close()


if __name__ == "__main__":
    init_db()

# KI-Ende