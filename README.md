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
![License](https://img.shields.io/badge/License-MIT-yellow.svg)

</p>

---

## Table of Contents

- [Overview](#overview)
- [Features](#features)
- [Tech Stack](#tech-stack)
- [Application Architecture](#application-architecture)
- [Project Structure](#project-structure)
- [Database Design](#database-design)
- [Database Schema](#database-schema)
- [Installation](#installation)
- [Running The Application](#running-the-application)
- [API Endpoints](#api-endpoints)
- [API Examples](#api-examples)
- [SQL Queries Tested](#sql-queries-tested)
- [Optional Features Implemented](#-optional-features-implemented)
- [Testing](#testing)
- [Key Backend Concepts Demonstrated](#key-backend-concepts-demonstrated)
- [Learning Outcomes](#learning-outcomes)
- [Future Improvements](#future-improvements)
- [Contributing](#contributing)
- [License](#license)
- [Author](#author)

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

> **Note:** Screenshots referenced in the [Testing](#testing) section (`1.png`, `2.png`, `3.png`) should live in the `images/` folder alongside `database.png`. Keep this structure in sync with what's actually committed to the repo so links don't break.

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

### macOS / Linux

```bash
source .venv/bin/activate
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

| Method | Endpoint | Description | Success Code | Error Codes |
|-|-|-|-|-|
|GET|/|API information|200|—|
|GET|/health|Health check|200|—|
|GET|/tasks|Get all tasks|200|422 (invalid query param)|
|GET|/tasks/{id}|Get task by ID|200|404 (task not found)|
|POST|/tasks|Create task|201|422 (validation error)|
|PUT|/tasks/{id}|Update task|200|404 (task not found), 422 (validation error)|
|DELETE|/tasks/{id}|Delete task|200|404 (task not found)|
|GET|/stats|Task statistics|200|—|
|POST|/reset|Reset tasks|200|—|

### Example error response

```json
{
  "detail": "Task with id 42 not found"
}
```

### Example validation error response (422)

```json
{
  "detail": [
    {
      "loc": ["body", "title"],
      "msg": "field required",
      "type": "value_error.missing"
    }
  ]
}
```

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

Response (`201 Created`):

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

Response (`200 OK`) or `404 Not Found` if the ID doesn't exist.

---

## Delete Task

```
DELETE /tasks/4
```

Response (`200 OK`):

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

# ⭐ Optional Features Implemented

In addition to the core CRUD requirements, the following optional features have been implemented using SQL queries.

---

## 🔍 Search Tasks

Search tasks by title using SQL's `LIKE` operator.

### Endpoint

```http
GET /tasks?search=milk
```

### Example

```http
GET /tasks?search=learn
```

### SQL Query

```sql
SELECT * FROM tasks
WHERE title LIKE '%learn%'
ORDER BY title ASC;
```

### Example Response

```json
[
  {
    "id": 1,
    "title": "Learn FastAPI",
    "done": false,
    "created_at": "2026-07-23 15:10:20",
    "updated_at": "2026-07-23 15:10:20"
  }
]
```

---

## ✅ Filter Tasks by Completion Status

Retrieve only completed or pending tasks.

### Endpoint

```http
GET /tasks?done=true
```

or

```http
GET /tasks?done=false
```

### SQL Query

```sql
SELECT * FROM tasks
WHERE done = ?
ORDER BY title ASC;
```

### Example Response

```json
[
  {
    "id": 2,
    "title": "Learn SQLite",
    "done": true
  }
]
```

---

## 🔤 Alphabetical Sorting

All task lists are automatically sorted alphabetically by title.

### SQL Query

```sql
SELECT * FROM tasks
ORDER BY title ASC;
```

---

## 📊 Task Statistics

Retrieve summary statistics directly from SQLite using SQL aggregate functions.

### Endpoint

```http
GET /stats
```

### SQL Queries

```sql
SELECT COUNT(*) FROM tasks;
```

```sql
SELECT COUNT(*) FROM tasks
WHERE done = 1;
```

```sql
SELECT COUNT(*) FROM tasks
WHERE done = 0;
```

### Example Response

```json
{
  "total": 8,
  "completed": 3,
  "pending": 5
}
```

---

## 🕒 Automatic Timestamps

Each task stores creation and last update timestamps.

### Database Schema

```sql
created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
```

### Update Query

Whenever a task is updated, the `updated_at` column is automatically refreshed.

```sql
UPDATE tasks
SET
    title = ?,
    done = ?,
    updated_at = CURRENT_TIMESTAMP
WHERE id = ?;
```

---

## 💾 SQL Features Used

| Feature | SQL Statement |
|---------|---------------|
| Search | `LIKE` |
| Filtering | `WHERE` |
| Sorting | `ORDER BY` |
| Statistics | `COUNT(*)` |
| Insert | `INSERT INTO` |
| Update | `UPDATE` |
| Delete | `DELETE` |
| Retrieve | `SELECT` |
| Parameterized Queries | `?` placeholders |

---

## 📌 Sample API Requests

### Get all tasks

```http
GET /tasks
```

### Search tasks

```http
GET /tasks?search=sqlite
```

### Filter completed tasks

```http
GET /tasks?done=true
```

### Filter pending tasks

```http
GET /tasks?done=false
```

### Get task statistics

```http
GET /stats
```

---

## 🚀 Key Improvements

- Persistent storage using SQLite
- SQL-based CRUD operations
- Parameterized queries to prevent SQL Injection
- Search functionality using `LIKE`
- Filtering using SQL `WHERE`
- Automatic alphabetical sorting
- SQL aggregate functions (`COUNT`)
- Automatic timestamps (`created_at`, `updated_at`)
- Clean RESTful API built with FastAPI

---

### Database

![Database](images/database.png)
*Accessed through Swagger UI*

![Task.db](images/database.png)
*Accessed through SQL viewer / DB Browser for SQLite*

---

# Testing

The API was tested using:

- Swagger UI
- Curl
- Postman

## Swagger UI

![Swagger UI](images/1.png)

## Sample curl commands

```bash
# Get all tasks
curl -X GET http://127.0.0.1:8000/tasks

# Create a task
curl -X POST http://127.0.0.1:8000/tasks \
  -H "Content-Type: application/json" \
  -d '{"title": "Complete backend assignment"}'

# Update a task
curl -X PUT http://127.0.0.1:8000/tasks/4 \
  -H "Content-Type: application/json" \
  -d '{"title": "Complete SQLite integration", "done": true}'

# Delete a task
curl -X DELETE http://127.0.0.1:8000/tasks/4
```

## Persistence testing

1. Created tasks through API
2. Restarted FastAPI server
3. Called `GET /tasks`
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
- Async database operations

---

# Contributing

This is a personal learning project built to practice backend engineering and API design. It's not currently set up to accept external contributions, but feedback, suggestions, and issue reports are welcome — feel free to open an issue if you spot a bug or have an idea for improvement.

---

# License

This project is licensed under the **MIT License**. See the [LICENSE](LICENSE) file for details.

You are free to use, copy, modify, and distribute this code for educational or personal purposes, provided the original copyright notice is retained.

---

# Author

**Rubab Ftaima**
GitHub: [RubabFatima2](https://github.com/RubabFatima2)