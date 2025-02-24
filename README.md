# Travelator Database API

A FastAPI-based service that provides activity and itinerary recommendations for travelers.

## Features

- Activity recommendations based on city, time of day, and group type
- Itinerary generation based on user preferences
- RESTful API with JSON responses
- Comprehensive test suite with high coverage
- Input validation using Pydantic models

## Setup

1. Create and activate a virtual environment:
```bash
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

## Running the Service

Start the service using uvicorn:
```bash
# Default port (8000)
uvicorn main:app --reload

# Specify a different port (e.g., 8001)
uvicorn main:app --reload --port 8001

# Specify host and port
uvicorn main:app --reload --host 0.0.0.0 --port 8001
```

The API will be available at:
- Default: `http://localhost:8000`
- Custom port: `http://localhost:PORT`

### Troubleshooting

If you see "Address already in use" error:
1. Choose a different port using `--port`
2. Or find and stop the process using port 8000:
```bash
# Find process using port 8000
lsof -i :8000

# Kill the process
kill -9 <PID>
```

## API Endpoints

### GET /activities
Request activities based on city, time of day, and group type.

Example request:
```json
{
    "city": "London",
    "timeOfDay": ["Morning", "Afternoon"],
    "group": "Family"
}
```

### POST /itinerary
Generate an itinerary based on user preferences.

Example request:
```json
{
    "city": "London",
    "preferences": [
        {
            "liked": ["Museum", "Park"],
            "disliked": ["Shopping"]
        }
    ]
}
```

## Development

### Running Tests

Run the test suite:
```bash
pytest
```

Run with coverage report:
```bash
pytest --cov=. --cov-report=term-missing
```

### Code Quality

Run flake8 for code style checking:
```bash
flake8 .
```

## Project Structure

- `main.py` - FastAPI application and route handlers
- `models.py` - Pydantic models for request/response validation
- `tests/` - Test suite
  - `test_models.py` - Model validation tests
  - `test_main.py` - API endpoint tests

## Dependencies

Main dependencies:
- FastAPI 0.109.2
- Pydantic 2.10.6
- Uvicorn 0.27.1
- HTTPX 0.26.0

Development dependencies:
- Pytest 8.0.0
- Pytest-asyncio 0.23.5
- Pytest-cov 4.1.0
- Flake8 7.0.0

## CI/CD

The project uses GitHub Actions for:
- Code style checking (flake8)
- Running tests with coverage
- Building and pushing Docker image

See `.github/workflows/build.yml` for details.