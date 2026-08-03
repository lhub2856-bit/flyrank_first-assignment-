from fastapi import FastAPI, HTTPException
from sqlmodel import SQLModel, Field, create_engine, Session, select
from typing import Optional
from pydantic import BaseModel
import os
from dotenv import load_dotenv
load_dotenv()

app = FastAPI()
DATABASE_URL = os.getenv("DATABASE_URL")
engine = create_engine(DATABASE_URL, echo=False)


class Task(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    title: str
    done: bool = False


@app.on_event("startup")
def on_startup():
    SQLModel.metadata.create_all(engine)

    with Session(engine) as session:
        existing = session.exec(select(Task)).first()
        if not existing:
            example_tasks = [
                Task(title="Buy milk", done=False),
                Task(title="Clean house", done=True),
                Task(title="Learn FastAPI", done=False),
            ]
            for task in example_tasks:
                session.add(task)
            session.commit()


@app.get("/")
def read_root():
    return {"name": "Task API", "version": "2.0", "endpoints": ["/tasks"]}


@app.get("/health")
def health_check():
    return {"status": "ok"}


@app.get("/tasks")
def get_tasks():
    with Session(engine) as session:
        tasks = session.exec(select(Task)).all()
        return tasks


@app.get("/tasks/{task_id}")
def get_task(task_id: int):
    with Session(engine) as session:
        task = session.get(Task, task_id)
        if not task:
            raise HTTPException(status_code=404, detail=f"Task {task_id} not found")
        return task
class TaskCreate(BaseModel):
    title: str


@app.post("/tasks", status_code=201)
def create_task(task_data: TaskCreate):
    if not task_data.title or task_data.title.strip() == "":
        raise HTTPException(status_code=400, detail="Title is required")

    with Session(engine) as session:
        new_task = Task(title=task_data.title, done=False)
        session.add(new_task)
        session.commit()
        session.refresh(new_task)
        return new_task   
class TaskUpdate(BaseModel):
    title: str
    done: bool = False


@app.put("/tasks/{task_id}")
def update_task(task_id: int, updated: TaskUpdate):
    if not updated.title or updated.title.strip() == "":
        raise HTTPException(status_code=400, detail="Title is required")

    with Session(engine) as session:
        task = session.get(Task, task_id)
        if not task:
            raise HTTPException(status_code=404, detail=f"Task {task_id} not found")

        task.title = updated.title
        task.done = updated.done
        session.add(task)
        session.commit()
        session.refresh(task)
        return task


@app.delete("/tasks/{task_id}", status_code=204)
def delete_task(task_id: int):
    with Session(engine) as session:
        task = session.get(Task, task_id)
        if not task:
            raise HTTPException(status_code=404, detail=f"Task {task_id} not found")

        session.delete(task)
        session.commit()
        return     