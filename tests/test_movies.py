import os
import csv
import pytest
from run import app  # Importa o app Flask
from app.extensions import db
from app.models.movies import MoviesData
from app.schemas.movies import MovieRecord
from app.services.movies import get_producers_with_longest_and_shortest_intervals, process_csv_to_movies

@pytest.fixture(autouse=True)
def app_context():
    with app.app_context():
        yield

@pytest.fixture
def temp_csv(tmp_path):
    csv_path = tmp_path / "movies.csv"
    data = [
        ["year", "studios", "title", "producers", "winner"],
        ["1990", "Warner", "Movie A", "John Doe", "True"],
        ["1995", "Universal", "Movie B", "Jane Doe", "False"]
    ]
    with open(csv_path, "w", encoding="utf-8", newline="") as f:
        writer = csv.writer(f, delimiter=";")
        writer.writerows(data)
    return csv_path

@pytest.fixture
def temp_invalid_csv(tmp_path):
    csv_path = tmp_path / "movies_inv.csv"
    data = [
        ["year", "studios", "title", "producers", "winner"],
        ["1990", "Warner", "Movie A", "ok", "True"],
        ["1995", "Universal", "Movie B", "Jane Doe", "False"]
    ]
    with open(csv_path, "w", encoding="utf-8", newline="") as f:
        writer = csv.writer(f, delimiter=";")
        writer.writerows(data)
    return csv_path

@pytest.fixture
def clear_db():
    db.session.query(MoviesData).delete()
    db.session.commit()
    yield
    db.session.query(MoviesData).delete()
    db.session.commit()

def test_process_csv_to_movies(temp_csv, clear_db):
    response = process_csv_to_movies(str(temp_csv))
    assert response == {"message": "CSV imported successfully"}
    movies = MoviesData.query.all()
    for movie in movies:
        assert MovieRecord.model_validate(movie)

def test_process_invalid_csv(temp_invalid_csv, clear_db):
    response = process_csv_to_movies(str(temp_invalid_csv))
    assert response == {"message": "CSV imported successfully"}
    movies = MoviesData.query.all()
    assert len(movies) == 0
    invalid_file = str(temp_invalid_csv).replace(".csv", "_invalid.csv")
    assert os.path.exists(invalid_file)
    with open(invalid_file, "r", encoding="utf-8") as f:
        reader = csv.DictReader(f, delimiter=";")
        invalid_rows = list(reader)
        assert len(invalid_rows) > 0
        for row in invalid_rows:
            assert "errors" in row

def test_get_produtores_com_intervalos(clear_db):
    db.session.add_all([
        MoviesData(year=2000, title="A", studios="X", producers="John", winner=True),
        MoviesData(year=2005, title="B", studios="Y", producers="John", winner=True),
        MoviesData(year=2010, title="C", studios="X", producers="Jane", winner=True),
        MoviesData(year=2012, title="D", studios="Y", producers="Jane", winner=True),
    ])
    db.session.commit()
    produtor_max, max_int, produtor_min, min_int = get_producers_with_longest_and_shortest_intervals()
    assert produtor_max == "John"
    assert max_int == 5
    assert produtor_min == "Jane"
    assert min_int == 2