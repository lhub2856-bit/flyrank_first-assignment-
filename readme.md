# Task API

A simple CRUD API for managing a to-do list, built with Python, FastAPI, and PostgreSQL.

## What This Is

This project implements Create, Read, Update, and Delete operations for tasks. Originally built with an in-memory store (Assignment 1), then SQLite (Assignment 2). This version (Assignment 3) swaps SQLite for a real PostgreSQL database running in Docker, with the whole stack (app + database) started using a single `docker compose up` command.

## Architecture Proof: Only the Connection Changed

The whole point of this assignment was to prove that switching storage backends doesn't require touching the service or route logic — only the data layer connection changes.

**What changed in `main.py`:**
```python
# Before (SQLite):
sqlite_file_name = "tasks.db"
sqlite_url = f"sqlite:///{sqlite_file_name}"
engine = create_engine(sqlite_url, echo=False)

# After (PostgreSQL via .env):
DATABASE_URL = os.getenv("DATABASE_URL")
engine = create_engine(DATABASE_URL, echo=False)
```

**What did NOT change:** the `Task` model, all routes (`GET /tasks`, `GET /tasks/{id}`, `POST /tasks`, `PUT /tasks/{id}`, `DELETE /tasks/{id}`), the startup seeding logic, and all business logic (validation, error handling). Because the app uses **SQLModel** (built on SQLAlchemy), the engine only cares about the connection string — the rest of the code works identically against SQLite or PostgreSQL.

This is a genuine, honest confirmation: the service and routes are unchanged, word for word.

## Project Structure

```
flyrank_crudapi/
├── main.py                 # FastAPI app, models, routes (unchanged since A2)
├── db/
│   └── init.sql            # Creates the `task` table on first Postgres startup
├── Dockerfile               # Builds the FastAPI app image
├── docker-compose.yml       # Runs app + Postgres together
├── requirements.txt
├── .env.example             # Template with placeholder password (committed)
└── README.md
```

## How to Run

1. Copy `.env.example` to `.env` and set your own password:
   ```
   DATABASE_URL=postgresql://postgres:<your_password_here>@db:5432/myappdb
   ```
2. Start the whole stack:
   ```bash
   docker compose up --build
   ```
3. The API will be available at `http://127.0.0.1:8000`. Interactive docs at `http://127.0.0.1:8000/docs`.

Note: inside `docker-compose.yml`, the app connects to the database using the service name `db` (not `localhost`), since containers on the same Docker network communicate by service name.

## Database Setup

- PostgreSQL 16 runs in a Docker container (`my-postgres`) with a **named volume** (`pgdata`) mounted at `/var/lib/postgresql/data`, so data survives container restarts and recreation.
- The table is created automatically on first startup via `db/init.sql`, mounted into Postgres's `docker-entrypoint-initdb.d` folder:
  ```sql
  CREATE TABLE IF NOT EXISTS task (
      id SERIAL PRIMARY KEY,
      title TEXT NOT NULL,
      done BOOLEAN NOT NULL DEFAULT FALSE
  );
  ```

## Environment Variables

| Variable | Description |
|---|---|
| `DATABASE_URL` | Full PostgreSQL connection string, read via `python-dotenv` in `main.py` |

`.env` is listed in `.gitignore` and is never committed. `.env.example` is committed with a placeholder password so anyone cloning the repo knows what variable to set.

## Persistence Proof

To confirm data survives a full restart (not just an app restart, but a container restart too):

1. Started the stack with `docker compose up --build`.
2. Confirmed the 3 seeded tasks were served from Postgres at `GET /tasks`.
3. Created a new task via `POST /tasks` (`{"title": "Persistence test task"}`) using the Swagger UI at `/docs`. Response confirmed `id: 4` was created.
4. Fully stopped the stack: `docker compose down` (this removes the containers but **not** the named volume — `-v` was deliberately not used).
5. Restarted the stack: `docker compose up`.
6. Postgres logs on restart showed: `"PostgreSQL Database directory appears to contain a database; Skipping initialization"` — confirming the volume's existing data was reused, not recreated from scratch.
7. Refreshed `GET /tasks` — all 4 tasks, including the "Persistence test task" (`id: 4`), were still present.

This confirms persistence works across both an app restart and a full container/stack restart.

## Notes / Gotchas Encountered

- The official `postgres:latest` image (Postgres 18) had a startup conflict with the mount path on this machine, so `postgres:16` was used instead — a known, stable, pinned version rather than `latest` (also better practice for reproducibility).
- A locally-installed Windows PostgreSQL service (`postgresql-x64-17`) was already listening on port 5432, causing an intermittent password authentication error when the app tried to connect through Docker's port mapping. Stopping that Windows service resolved the conflict.
- Inside `docker-compose.yml`, the connection host must be the service name `db`, not `localhost`, since the app and database run in separate containers on the same Docker network.

## Stretch Goals

- [ ] Redis added to `docker-compose.yml` and pinged from the app
- [ ] Index added + `EXPLAIN ANALYZE` before/after comparison on a seeded table

(Not yet completed — left for a future iteration.)