# Task API

A simple CRUD API for managing a to-do list, built with Python, FastAPI, and SQLite.

## What This Is
This project implements Create, Read, Update, and Delete operations for tasks using a SQLite database. Data now persists even after the server restarts. Built as part of the FlyRank internship Week 3 assignment.

## Why SQLite
SQLite was chosen because it requires no separate database server or installation — it stores everything in a single file (`tasks.db`) on disk. This makes it ideal for learning and small projects, while still using real SQL queries.

## Where the Database File Is Stored
The database file `tasks.db` is created automatically in the project's root folder the first time the app runs.

## How to Run

1. Install dependencies:
pip install fastapi uvicorn sqlmodel


2. Run the server:

uvicorn main:app --reload


3. Open your browser at `http://localhost:8000`

The database file and table are created automatically. Three example tasks are inserted only if the table is empty.

## Endpoints

| Method | Endpoint          | Description         |
|--------|-------------------|----------------------|
| GET    | /                 | API info             |
| GET    | /health           | Health check          |
| GET    | /tasks            | List all tasks        |
| GET    | /tasks/{id}       | Get a single task     |
| POST   | /tasks            | Create a new task     |
| PUT    | /tasks/{id}       | Update a task          |
| DELETE | /tasks/{id}       | Delete a task           |

## Swagger UI
Interactive documentation available at `http://localhost:8000/docs`
## Example SQL Query
```sql
SELECT * FROM task WHERE done = 1;
```
This returns only the tasks that are marked as completed.

