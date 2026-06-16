from sqlalchemy import Column, Integer, String, Date, DECIMAL, ForeignKey
from database import Base


class DBUser(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    name = Column(String(20), nullable=False)


class DBMovies(Base):


    __tablename__ = "movies"
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    api_movie_id = Column(Integer, nullable=False, unique=True)
    title = Column(String(50), nullable=False)
    description = Column(String(500), nullable=True)
    release_date = Column(Date, nullable=True)





class DBSwipe(Base):
    __tablename__ = "swipes"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    user_id  = Column(Integer, ForeignKey("users.id"), nullable=False)
    movie_id = Column(Integer, ForeignKey("movies.id"), nullable=False)
    swipe_type  = Column(String(10), nullable=False)


class DBGenre(Base):
    __tablename__ = "genres"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    genre = Column(String(50), nullable=False, unique=True)


class DBMovieGenre(Base):
    __tablename__ = "movie_genres"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    genre_id = Column(Integer, ForeignKey("genres.id"), nullable=False)
    movie_id = Column(Integer, ForeignKey("movies.id"), nullable=False)


class DBMovieDetails(Base):
    __tablename__ = "movie_details"

    movie_id = Column(Integer, ForeignKey("movies.id"), primary_key=True)
    dauer = Column(Integer, nullable=True)
    erlaubtes_alter = Column(Integer, nullable=True)
    bewertung = Column(DECIMAL, nullable=True)