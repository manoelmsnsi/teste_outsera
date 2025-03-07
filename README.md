
# Teste Outsera

This project is a Flask-based application for managing movie data, including importing data from CSV files and calculating intervals between awards for producers.

## Project Structure

- `app/`: Contains the main application code.
  - `module/`: Contains the module application code.
    - `controller.py`: Contains the route handlers.
    - `model.py`: Contains the database models.
    - `reposittory.py`: Contém as classes responsáveis pelo acesso aos dados (Repository).
    - `schema.py`: Contains Pydantic models for data validation.
    - `service.py`: Contains the business logic.
  - `extensions.py`: Configures Flask extensions.
  - `routes.py`: Registers the application routes.
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
   <br>if poetry
   ```bash
   poetry install
   ```
   
   if pip linux
    ```bash
   python -m venv .venv && source .venv/bin/activate && pip install -r requirements.txt
   ```
   if pip Windows
      ```bash
   python -m venv .venv && .venv\Scripts\activate && pip install -r requirements.txt
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
if using poetry
```bash
poetry run pytest
```
if using python
```bash
python -m pytest
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
      "data": {
        "max": [
          {
            "followingWin": 2050,
            "interval": 31,
            "previousWin": 2019,
            "producer": "teste max"
          }
        ],
        "min": [
          {
            "followingWin": 2020,
            "interval": 1,
            "previousWin": 2019,
            "producer": "teste min"
          }
        ]
      },
      "detail": null,
      "status_code": 200
    }
    ```

## CSV Import

The application automatically imports movie data from a CSV file located at `documents/movielist.csv` when it starts. Invalid records are saved to a separate file with `_invalid.csv` suffix.

## License

This project is licensed under the MIT License.
