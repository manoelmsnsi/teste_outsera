# Use the official Python image from the Docker Hub
FROM python:3.13-slim

# Set environment variables
ENV PYTHONUNBUFFERED=1

# Set the working directory
WORKDIR /app

# Copy the project files into the container
COPY app/ /app

# Install Poetry
RUN pip install poetry

COPY pyproject.toml /app
COPY poetry.lock /app

# Install dependencies
RUN poetry config virtualenvs.create false && poetry install --no-interaction --only main

COPY run.py /app


# Expose the port the app runs on
EXPOSE 5000

# Run the application with Gunicorn
CMD ["gunicorn", "-b", "0.0.0.0:5000", "run:app"]
