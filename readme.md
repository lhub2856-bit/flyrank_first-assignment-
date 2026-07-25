# Task API

A simple CRUD API for managing a to-do list, built with Python and FastAPI.

## What This Is
This project implements Create, Read, Update, and Delete operations for tasks using an in-memory list (no database yet). Built as part of the FlyRank internship Week 2 assignment.

## How to Run

1. Install dependencies:
pip install fastapi uvicorn
2. Run the server:
uvicorn main:app --reload
3. Open your browser at `http://localhost:8000`

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
