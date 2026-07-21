# Task API

A simple RESTful Task Management API built with **FastAPI**. This project demonstrates the implementation of CRUD (Create, Read, Update, Delete) operations using in-memory storage and Pydantic models for request validation.

## Features

- View all tasks
- Retrieve a task by ID
- Create a new task
- Update an existing task
- Delete a task
- Request validation using Pydantic
- Automatic interactive API documentation with Swagger UI

## Tech Stack

- Python 3.x
- FastAPI
- Pydantic
- Uvicorn

## Project Structure

```
.
├── main.py              # Application entry point
├── pyproject.toml       # Project dependencies
├── uv.lock              # Dependency lock file
├── README.md
└── .gitignore
```

## Installation

### Clone the repository

```bash
git clone <repository-url>
cd <repository-folder>
```

### Create a virtual environment

```bash
uv venv
```

### Activate the virtual environment

**Windows (PowerShell)**

```powershell
.venv\Scripts\Activate.ps1
```

**Windows (Command Prompt)**

```cmd
.venv\Scripts\activate.bat
```

### Install dependencies

```bash
uv sync
```

or

```bash
uv add fastapi "uvicorn[standard]"
```

## Running the Application

```bash
uv run uvicorn main:app --reload
```

The server will start at:

```
http://127.0.0.1:8000
```

## API Documentation

Swagger UI:

```
http://127.0.0.1:8000/docs
```

ReDoc:

```
http://127.0.0.1:8000/redoc
```

## Available Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/` | API information |
| GET | `/health` | Health check |
| GET | `/tasks` | Retrieve all tasks |
| GET | `/tasks/{id}` | Retrieve a task by ID |
| POST | `/tasks` | Create a new task |
| PUT | `/tasks/{id}` | Update an existing task |
| DELETE | `/tasks/{id}` | Delete a task |

## Example Request

### Create a Task

```http
POST /tasks
```

Request Body

```json
{
  "title": "Complete FastAPI assignment"
}
```

Example Response

```json
{
  "id": 4,
  "title": "Complete FastAPI assignment",
  "done": false
}
```

## Testing

The API can be tested using:

- Swagger UI
- curl
- Postman
- Insomnia

## Future Improvements

- Persistent database integration (PostgreSQL/SQLite)
- UUID-based task identifiers
- Input validation and custom error handling
- Pagination and filtering
- Authentication and authorization
- Unit and integration testing

## License

This project is intended for educational and learning purposes.