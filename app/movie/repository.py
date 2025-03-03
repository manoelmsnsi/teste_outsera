# movies_repository.py
from app.extensions import db
from typing import List, Tuple
from app.movie.model import MoviesData

class MoviesRepository:
    def __init__(self, session=db.session):
        self.session = session

    def add_movie(self, movie: MoviesData):
        self.session.add(movie)

    def commit(self):
        self.session.commit()

    def rollback(self):
        self.session.rollback()

    def get_awards(self) -> List[Tuple[str, int]]:
        """
        Retorna uma lista de tuplas com (producer, year) de filmes premiados.
        """
        return (
            self.session.query(MoviesData.producers, MoviesData.year)
            .filter(MoviesData.winner == True)
            .order_by(MoviesData.producers, MoviesData.year)
            .all()
        )
