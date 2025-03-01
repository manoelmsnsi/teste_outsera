
# Teste Outsera

This project is a Flask-based application for managing movie data, including importing data from CSV files and calculating intervals between awards for producers.

## Project Structure

- `app/`: Contains the main application code.
  - `controllers/`: Contains the route handlers.
  - `extensions.py`: Configures Flask extensions.
  - `models/`: Contains the database models.
  - `routes.py`: Registers the application routes.
  - `schemas/`: Contains Pydantic models for data validation.
  - `services/`: Contains the business logic.
- `config.py`: Configuration settings for different environments.
- `run.py`: Entry point for running the application.
- `tests/`: Contains the test cases.
- `pyproject.toml`: Project dependencies and settings.

## Setup

1. **Clone the repository:**
   ```bash
   git clone <repository_url>
   cd teste_outsera
   ```

2. **Install dependencies:**
   ```bash
   poetry install
   ```

3. **Set up environment variables:**
   Create a `.env` file in the project root and add the necessary environment variables:
   ```env
   SECRET_KEY=your_secret_key
   DEV_DATABASE_URI=sqlite:///dev.db
   PROD_DATABASE_URI=sqlite:///prod.db
   TEST_DATABASE_URI=sqlite:///test.db
   ```

4. **Run the application:**
   ```bash
   poetry run python run.py
   ```

## Running Tests

To run the tests, use the following command:
```bash
poetry run pytest
```

## API Endpoints

### Health Check

- **GET** `/api/health/`
  - Response: `{"status": "ok"}`

### Movies

- **GET** `/api/movies/awarded-producer`
  - Response: 
    ```json
    {
      "status_code": 200,
      "data": {
        "producer_with_longest_interval": {
          "producer": "John",
          "interval": 5
        },
        "producer_with_shortest_interval": {
          "producer": "Jane",
          "interval": 2
        }
      },
      "detail": null
    }
    ```

## CSV Import

The application automatically imports movie data from a CSV file located at `documents/movielist.csv` when it starts. Invalid records are saved to a separate file with `_invalid.csv` suffix.

## License

This project is licensed under the MIT License.
