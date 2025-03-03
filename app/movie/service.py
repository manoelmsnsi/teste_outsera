import csv
import logging
from typing import List, Tuple
from pydantic import ValidationError

from app.movie.model import MoviesData
from app.movie.repository import MoviesRepository
from app.movie.schema import AwardedProducerResponse, MovieRecord  # Pydantic model

# Colunas obrigatórias para validação
REQUIRED_COLUMNS = {"year", "studios", "title", "producers", "winner"}

def process_csv_to_movies(file_path) -> dict:
    """
    Lê um arquivo CSV, valida a estrutura usando Pydantic e insere apenas os registros válidos.
    Registros inválidos são salvos em um arquivo separado para posterior análise.
    """
    invalid_records = []
    repo = MoviesRepository()

    try:
        logging.info("Iniciando importação do CSV")

        with open(file_path, newline="", encoding="utf-8") as csvfile:
            reader = csv.DictReader(csvfile, delimiter=';')

            if not REQUIRED_COLUMNS.issubset(reader.fieldnames):
                raise ValueError(
                    f"CSV inválido. Esperado: {REQUIRED_COLUMNS}, Encontrado: {set(reader.fieldnames)}"
                )

            fieldnames = reader.fieldnames

            for index, row in enumerate(reader):
                try:
                    validated_movie = MovieRecord.model_validate(row)
                    record = MoviesData(
                        year=int(validated_movie.year),
                        title=validated_movie.title,
                        studios=validated_movie.studios,
                        producers=validated_movie.producers,
                        winner=validated_movie.winner
                    )
                    repo.add_movie(record)

                except (ValidationError, TypeError, ValueError) as e:
                    error_msg = str(e)
                    logging.error(f"Erro de validação no registro {row}: {error_msg}")
                    row["errors"] = f"{error_msg} (linha {index})"
                    invalid_records.append(row)

            repo.commit()

        # Salva registros inválidos em um arquivo separado
        if invalid_records:
            invalid_file_path = file_path.replace(".csv", "_invalid.csv")
            with open(invalid_file_path, "w", newline="", encoding="utf-8") as invalid_file:
                writer_fieldnames = fieldnames + ["errors"]
                writer = csv.DictWriter(invalid_file, fieldnames=writer_fieldnames, delimiter=";")
                writer.writeheader()
                writer.writerows(invalid_records)
            logging.info(f"Registros inválidos salvos em {invalid_file_path}")

        return {"message": "CSV imported successfully"}

    except Exception as e:
        repo.rollback()
        logging.error(f"Erro ao importar CSV: {e}")
        return {"error": str(e)}


def get_producers_with_longest_and_shortest_intervals() -> Tuple[List[AwardedProducerResponse], List[AwardedProducerResponse]]:
    """
    Recupera os produtores com os maiores e menores intervalos entre vitórias,
    retornando todos os registros que possuam o mesmo intervalo máximo ou mínimo.
    """
    repo = MoviesRepository()
    awards = repo.get_awards()

    if not awards:
        return [], []

    # Agrupa os anos de vitória por produtor
    producers = {}
    for producer, year in awards:
        if producer not in producers:
            producers[producer] = []
        producers[producer].append(year)

    # Calcula os intervalos entre vitórias
    intervals: List[AwardedProducerResponse] = []
    for producer, years in producers.items():
        if len(years) < 2:
            continue  # Precisa de pelo menos duas vitórias para calcular um intervalo
        years.sort()
        for i in range(1, len(years)):
            interval_val = years[i] - years[i - 1]
            intervals.append(AwardedProducerResponse(
                producer=producer,
                interval=interval_val,
                previousWin=years[i - 1],
                followingWin=years[i]
            ))

    if not intervals:
        return [], []

    # Determina os valores máximo e mínimo dos intervalos
    max_interval_value = max(record.interval for record in intervals)
    min_interval_value = min(record.interval for record in intervals)

    # Filtra registros com os intervalos máximo e mínimo
    shortest_intervals = [record for record in intervals if record.interval == min_interval_value]
    longest_intervals = [record for record in intervals if record.interval == max_interval_value]

    return shortest_intervals, longest_intervals
