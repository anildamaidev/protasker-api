from fastapi import FastAPI
from pydantic import BaseModel
from database import connection, cursor

app = FastAPI(
    title="ProTasker API",
    description="A simple Task Management API built using FastAPI and SQLite.",
    version="1.0.0"
)


class Task(BaseModel):
    title: str
    priority: str

@app.get("/")
def home():
    return {
        "message": "Welcome to ProTasker API"
    }


@app.post("/tasks")
def create_task(task: Task):

    cursor.execute(
        "INSERT INTO tasks(title, priority) VALUES(?, ?)",
        (task.title, task.priority)
    )

    connection.commit()

    task_id = cursor.lastrowid

    return {
        "message": "Task added",
        "task": {
            "id": task_id,
            "title": task.title,
            "priority": task.priority
        }
    }


@app.get("/tasks")
def get_tasks():

    cursor.execute("SELECT * FROM tasks")

    rows = cursor.fetchall()

    tasks = []

    for row in rows:
        tasks.append({
            "id": row[0],
            "title": row[1],
            "priority": row[2]
        })

    return {
        "tasks": tasks
    }


@app.get("/tasks/{task_id}")
def get_task(task_id: int):

    cursor.execute(
        "SELECT * FROM tasks WHERE id=?",
        (task_id,)
    )

    row = cursor.fetchone()

    if row is None:
        return {
            "error": "Task not found"
        }

    return {
        "id": row[0],
        "title": row[1],
        "priority": row[2]
    }


@app.put("/tasks/{task_id}")
def update_task(task_id: int, task: Task):

    cursor.execute(
        "UPDATE tasks SET title=?, priority=? WHERE id=?",
        (task.title, task.priority, task_id)
    )

    connection.commit()

    if cursor.rowcount == 0:
        return {
            "error": "Task not found"
        }

    return {
        "message": "Task updated",
        "task": {
            "id": task_id,
            "title": task.title,
            "priority": task.priority
        }
    }


@app.delete("/tasks/{task_id}")
def delete_task(task_id: int):

    cursor.execute(
        "DELETE FROM tasks WHERE id=?",
        (task_id,)
    )

    connection.commit()

    if cursor.rowcount == 0:
        return {
            "error": "Task not found"
        }

    return {
        "message": "Task deleted"
    }