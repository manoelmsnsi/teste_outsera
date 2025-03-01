import csv
import logging
from app.extensions import db
from pydantic import ValidationError

from app.models.movies import MoviesData
from app.schemas.movies import MovieRecord  # Import the Pydantic model

# Required columns for validation
REQUIRED_COLUMNS = {"year", "studios", "title", "producers", "winner"}

def process_csv_to_movies(file_path)-> dict:
    """
    Reads a CSV file, validates its structure using Pydantic, and inserts only valid records into the database.
    Invalid records are saved in a separate file for later processing.
    """
    invalid_records = []
    
    try:
        logging.info("Starting CSV import process")
        
        with open(file_path, newline="", encoding="utf-8") as csvfile:
            reader = csv.DictReader(csvfile, delimiter=';')
            
            if not REQUIRED_COLUMNS.issubset(reader.fieldnames):
                raise ValueError(
                    f"Invalid CSV. Expected: {REQUIRED_COLUMNS}, "
                    f"Found: {set(reader.fieldnames)}"
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
                    db.session.add(record)
                
                except (ValidationError, TypeError, ValueError) as e:
                    error_msg = str(e)
                    logging.error(f"Validation error in record {row}: {error_msg}")
                    row["errors"] = f"{error_msg} (line {index})"
                    invalid_records.append(row)
            
            db.session.commit()
        
        # Save invalid records to a separate file
        if invalid_records:
            invalid_file_path = file_path.replace(".csv", "_invalid.csv")
            with open(invalid_file_path, "w", newline="", encoding="utf-8") as invalid_file:
                writer_fieldnames = fieldnames + ["errors"]
                writer = csv.DictWriter(invalid_file, fieldnames=writer_fieldnames, delimiter=";")
                writer.writeheader()
                writer.writerows(invalid_records)
            logging.info(f"Invalid records saved to {invalid_file_path}")
        
        return {"message": "CSV imported successfully"}
    
    except Exception as e:
        db.session.rollback()
        logging.error(f"Error importing CSV: {e}")
        return {"error": str(e)}


def get_producers_with_longest_and_shortest_intervals()-> tuple:
    """
    Retrieves producers with the longest and shortest intervals between winning awards.
    """
    awards = db.session.query(
        MoviesData.producers,
        MoviesData.year
    ).filter(MoviesData.winner == True).order_by(MoviesData.producers, MoviesData.year).all()

    if not awards:
        return None, None, None, None

    producers = {}
    
    # Organize awards by producer
    for producer, year in awards:
        if producer not in producers:
            producers[producer] = []
        producers[producer].append(year)

    longest_interval = 0  # in years
    shortest_interval = float("inf")  # Start with a large interval (infinity)
    producer_with_longest_interval = None
    producer_with_shortest_interval = None
    
    for producer, years in producers.items():
        if len(years) < 2:
            continue
        
        years.sort()

        # Calculate intervals between consecutive awards
        for i in range(1, len(years)):
            interval = years[i] - years[i - 1]
            
            if interval > longest_interval:
                longest_interval = interval
                producer_with_longest_interval = producer
            
            if interval < shortest_interval:
                shortest_interval = interval
                producer_with_shortest_interval = producer
    
    return producer_with_longest_interval, longest_interval, producer_with_shortest_interval, shortest_interval
