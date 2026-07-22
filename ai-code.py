from fastapi import FastAPI, HTTPException, status, Query
from pydantic import BaseModel, Field
from typing import Optional

app = FastAPI(
    title="Task API",
    version="1.0",
    description="A simple CRUD Task API built with FastAPI."
)

# -----------------------------
# Models
# -----------------------------

class Task(BaseModel):
    id: int
    title: str
    done: bool


class TaskCreate(BaseModel):
    title: str = Field(..., min_length=1)


class TaskUpdate(BaseModel):
    title: Optional[str] = None
    done: Optional[bool] = None


# -----------------------------
# Initial Data
# -----------------------------

initial_tasks = [
    {"id": 1, "title": "Study FastAPI", "done": False},
    {"id": 2, "title": "Complete Assignment", "done": False},
    {"id": 3, "title": "Practice CRUD APIs", "done": True},
]

tasks = initial_tasks.copy()


# -----------------------------
# Stage 0
# -----------------------------

@app.get("/", summary="Welcome Message")
def hello():
    """Returns a welcome message."""
    return {
        "message": "Hello! Welcome to Task API",
        "name": "Task API",
        "version": "1.0",
        "endpoints": [
            "/tasks",
            "/health",
            "/stats",
            "/reset",
            "/docs"
        ]
    }


# -----------------------------
# Stage 1
# -----------------------------

@app.get("/health", summary="Health Check")
def health():
    """Checks whether the API is running."""
    return {"status": "ok"}


# -----------------------------
# Stage 2
# -----------------------------

@app.get("/tasks", summary="Get All Tasks")
def get_tasks(
    done: Optional[bool] = Query(None),
    search: Optional[str] = Query(None)
):
    """
    Returns all tasks.
    Optional filtering by completion status.
    Optional searching by title.
    """

    result = tasks

    if done is not None:
        result = [task for task in result if task["done"] == done]

    if search:
        result = [
            task
            for task in result
            if search.lower() in task["title"].lower()
        ]

    return result


@app.get("/tasks/{task_id}", summary="Get Single Task")
def get_task(task_id: int):
    """Returns a single task by ID."""

    for task in tasks:
        if task["id"] == task_id:
            return task

    raise HTTPException(
        status_code=404,
        detail=f"Task {task_id} not found"
    )


# -----------------------------
# Stage 3
# -----------------------------

@app.post(
    "/tasks",
    status_code=status.HTTP_201_CREATED,
    summary="Create Task"
)
def create_task(task: TaskCreate):
    """Creates a new task."""

    next_id = max(t["id"] for t in tasks) + 1 if tasks else 1

    new_task = {
        "id": next_id,
        "title": task.title,
        "done": False
    }

    tasks.append(new_task)

    return new_task


# -----------------------------
# Stage 4
# -----------------------------

@app.put("/tasks/{task_id}", summary="Update Task")
def update_task(task_id: int, updated: TaskUpdate):
    """Updates an existing task."""

    if updated.title is None and updated.done is None:
        raise HTTPException(
            status_code=400,
            detail="Request body cannot be empty."
        )

    for task in tasks:

        if task["id"] == task_id:

            if updated.title is not None:

                if updated.title.strip() == "":
                    raise HTTPException(
                        status_code=400,
                        detail="Title cannot be empty."
                    )

                task["title"] = updated.title

            if updated.done is not None:
                task["done"] = updated.done

            return task

    raise HTTPException(
        status_code=404,
        detail=f"Task {task_id} not found"
    )


@app.delete(
    "/tasks/{task_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Delete Task"
)
def delete_task(task_id: int):
    """Deletes a task."""

    for index, task in enumerate(tasks):

        if task["id"] == task_id:
            tasks.pop(index)
            return

    raise HTTPException(
        status_code=404,
        detail=f"Task {task_id} not found"
    )


# -----------------------------
# Optional Extras
# -----------------------------

@app.get("/stats", summary="Task Statistics")
def stats():
    """Returns task statistics."""

    total = len(tasks)
    done = len([t for t in tasks if t["done"]])
    open_tasks = total - done

    return {
        "total": total,
        "done": done,
        "open": open_tasks
    }


@app.post("/reset", summary="Reset Tasks")
def reset():
    """Restores the initial sample tasks."""

    global tasks
    tasks = initial_tasks.copy()

    return {
        "message": "Tasks reset successfully.",
        "tasks": tasks
    }