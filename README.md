# TaskFlow API

<p align="center">
  <b>A production-style RESTful Task Management API built with FastAPI and SQLite</b>
</p>

<p align="center">
  Backend project demonstrating CRUD operations, API design, request validation, database persistence, and clean separation between application logic and data storage.
</p>


<p align="center">

![Python](https://img.shields.io/badge/Python-3.10+-blue?logo=python)
![FastAPI](https://img.shields.io/badge/FastAPI-0.110+-009688?logo=fastapi)
![SQLite](https://img.shields.io/badge/SQLite-Database-003B57?logo=sqlite)
![Pydantic](https://img.shields.io/badge/Pydantic-Validation-E92063)
![Uvicorn](https://img.shields.io/badge/Uvicorn-ASGI-black)

</p>


---

# Overview

TaskFlow API is a backend REST API built using **FastAPI** that manages tasks through complete CRUD operations.

The project initially used an in-memory Python list for storing tasks. The storage layer was later upgraded to **SQLite**, allowing tasks to persist even after restarting the application.

The API contract remains unchanged while the database layer handles permanent storage.

This project demonstrates an important backend principle:

> The API defines what the application does.  
> The database defines where the application stores data.


---

# Features

## Core Features

- Create new tasks
- Retrieve all tasks
- Retrieve task by ID
- Update existing tasks
- Delete tasks
- Persistent SQLite database storage
- Automatic database initialization
- Automatic table creation
- Sample data insertion on first run
- Request validation using Pydantic models
- Interactive Swagger API documentation


## Additional Features

- Health check endpoint
- Task statistics endpoint
- Reset testing data endpoint
- SQL-based database operations


---

# Tech Stack

| Technology | Usage |
|---|---|
| Python | Backend programming language |
| FastAPI | REST API framework |
| Pydantic | Data validation and schemas |
| SQLite | Persistent relational database |
| SQL | Database queries |
| Uvicorn | Application server |
| Swagger UI | API testing documentation |


---

# Application Architecture

The application follows a simple layered backend structure:

```
Client
  |
  |
FastAPI Routes
(main.py)
  |
  |
Database Layer
(tasks.py)
  |
  |
SQLite Database
(tasks.db)
```


## Before Database Integration

```
Client
  |
API
  |
Python List
```

Data was lost after restarting the application.


## After Database Integration

```
Client
  |
API
  |
SQLite Database
```

Data survives application restarts.


---

# Project Structure

```
TaskFlow2/

│
├── main.py
│   └── FastAPI routes and API logic
│
├── tasks.py
│   └── SQLite database operations
│
├── tasks.db
│   └── SQLite database file
│
├── images/
│   └── database.png
│
├── pyproject.toml
│   └── Project dependencies
│
├── uv.lock
│   └── Dependency lock file
│
├── README.md
│
└── .gitignore
```


---

# Database Design

## Database Choice

SQLite was selected because:

- No external database server is required
- Lightweight and easy to configure
- Stored as a single file
- Supports real SQL queries
- Suitable for small backend applications


Database file:

```
tasks.db
```


The application automatically:

1. Creates the database if missing
2. Creates the tasks table
3. Inserts initial tasks only when the table is empty


---

# Database Schema

## Tasks Table

| Column | Type | Description |
|-|-|-|
| id | INTEGER | Primary key |
| title | TEXT | Task description |
| done | BOOLEAN | Completion status |


Example data:

| id | title | done |
|-|-|-|
|1|Learn FastAPI|0|
|2|Learn SQLite|0|
|3|Build Todo API|0|


---

# Installation

## Clone Repository

```bash
git clone <repository-url>

cd TaskFlow2
```


---

## Create Virtual Environment

```bash
uv venv
```


Activate environment:


### Windows

```powershell
.venv\Scripts\Activate.ps1
```


---

## Install Dependencies

```bash
uv sync
```


or:

```bash
uv add fastapi "uvicorn[standard]"
```


---

# Running The Application


Start server:

```bash
uv run uvicorn main:app --reload
```


Application runs at:

```
http://127.0.0.1:8000
```


Swagger documentation:

```
http://127.0.0.1:8000/docs
```


ReDoc:

```
http://127.0.0.1:8000/redoc
```


---

# API Endpoints


| Method | Endpoint | Description |
|-|-|-|
|GET|/|API information|
|GET|/health|Health check|
|GET|/tasks|Get all tasks|
|GET|/tasks/{id}|Get task by ID|
|POST|/tasks|Create task|
|PUT|/tasks/{id}|Update task|
|DELETE|/tasks/{id}|Delete task|
|GET|/stats|Task statistics|
|POST|/reset|Reset tasks|


---

# API Examples


## Create Task

### Request

```
POST /tasks
```


Body:

```json
{
"title":"Complete backend assignment"
}
```


Response:

```json
{
"id":4,
"title":"Complete backend assignment",
"done":false
}
```


---

## Update Task


```
PUT /tasks/4
```


Body:

```json
{
"title":"Complete SQLite integration",
"done":true
}
```


---

## Delete Task


```
DELETE /tasks/4
```


Response:

```json
{
"status":"Task deleted"
}
```


---

# SQL Queries Tested


## Fetch all tasks

```sql
SELECT * FROM tasks;
```


## Fetch completed tasks

```sql
SELECT *
FROM tasks
WHERE done = 1;
```


## Count tasks

```sql
SELECT COUNT(*)
FROM tasks;
```


## Update tasks

```sql
UPDATE tasks
SET done = 1;
```


## Delete completed tasks

```sql
DELETE FROM tasks
WHERE done = 1;
```





---

# Testing

The API was tested using:

- Swagger UI
- Curl
- Postman
---
## Swagger UI



![Swagger UI](images/1.png)
---
Persistence testing:

1. Created tasks through API
2. Restarted FastAPI server
3. Called GET `/tasks`
4. Verified data remained available


---

# Key Backend Concepts Demonstrated


## API Layer

Responsible for:

- Receiving requests
- Validating input
- Returning responses


## Database Layer

Responsible for:

- SQL queries
- Saving data
- Updating records


## Pydantic Models

Responsible for:

- Request schema definition
- Type validation
- Data conversion


---

# Learning Outcomes


Through this project, I learned:

- Designing REST APIs using FastAPI
- Working with request bodies
- Using Pydantic schemas
- Performing SQL CRUD operations
- Connecting applications with databases
- Separating routes from database logic
- Understanding persistence
- Writing professional backend documentation


---

# Future Improvements


Possible improvements:

- PostgreSQL migration
- Authentication and authorization
- Docker deployment
- Automated testing
- Database migrations
- Pagination
- Search and filtering
- Async database operations


---

# License

This project is created for educational and backend engineering practice purposes.