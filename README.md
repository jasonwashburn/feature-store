# Feature Store

A RESTful API service for storing and querying geospatial features built
with FastAPI and MongoDB.

## Overview

Feature Store is a Python-based web service that provides CRUD operations for
GeoJSON features with geospatial indexing and querying capabilities. It's
designed for applications that need to store, retrieve, and perform spatial
queries on geographic data.

## Features

- **CRUD Operations**: Create, read, update, and delete GeoJSON features
- **Geospatial Queries**: Find features that intersect with given geometries
- **MongoDB Integration**: Uses MongoDB with geospatial indexing for efficient
  spatial queries
- **FastAPI Framework**: Modern, fast web framework with automatic API documentation
- **Type Safety**: Built with Pydantic models for data validation and serialization
- **Docker Support**: Includes Docker Compose setup for easy deployment

## Supported Geometry Types

- Point
- LineString
- Polygon

## API Endpoints

- `GET /` - Welcome message
- `POST /features/` - Create a new feature
- `GET /features/` - Retrieve all features
- `GET /features/{feature_id}` - Retrieve a specific feature by ID
- `PUT /features/{feature_id}` - Update a feature by ID
- `DELETE /features/{feature_id}` - Delete a feature by ID
- `POST /features/geospatial/intersects` - Find features that intersect with a
  given polygon

## Quick Start

### Prerequisites

- Python 3.10+
- Poetry (for dependency management)
- Docker and Docker Compose (for MongoDB)

### Installation

1. Clone the repository:

```bash
git clone https://github.com/jasonwashburn/feature-store.git
cd feature-store
```

1. Install dependencies:

```bash
poetry install
```

1. Set up environment variables:
   Create a `.env` file with:

```env
MONGODB_USERNAME=your_username
MONGODB_PASSWORD=your_password
MONGODB_HOST=localhost
MONGODB_PORT=27017
```

1. Start MongoDB using Docker Compose:

```bash
docker-compose up -d
```

1. Run the application:

```bash
poetry run python src/feature_store/main.py
```

The API will be available at `http://localhost:8000` with automatic documentation
at `http://localhost:8000/docs`.

## Development

### Running Tests

```bash
# Run all tests
poetry run pytest

# Run with coverage
poetry run pytest --cov=src

# Run specific test types
poetry run pytest test/unit/
poetry run pytest test/e2e/
```

### Code Quality

This project uses several tools for code quality:

```bash
# Format code
poetry run black .

# Lint code
poetry run ruff check .

# Type checking
poetry run mypy .
```

### Pre-commit Hooks

Install pre-commit hooks to automatically run code quality checks:

```bash
poetry run pre-commit install
```

## Docker Services

The included `docker-compose.yml` provides:

- **MongoDB**: Document database with geospatial indexing
- **Mongo Express**: Web-based MongoDB administration interface (available at `http://localhost:8081`)

## Project Structure

```
src/feature_store/
├── main.py              # Application entry point
└── server/
    ├── app.py           # FastAPI application setup
    ├── database.py      # Database models and connection
    ├── models/
    │   └── geojson.py   # GeoJSON Pydantic models
    └── routes/
        └── features.py  # Feature API endpoints
```

## Author

Jason Washburn (<jason.washburn@gmail.com>)

