from fastapi import FastAPI, HTTPException, Path, Response
from pydantic import BaseModel, Field

app = FastAPI(title="Task Tracker API")

# In-memory store (starts empty; resets on server restart)
tasks: dict[int, dict] = {}
next_task_id = 1


def reset_store() -> None:
    """Reset in-memory tasks and ID counter (used by automated tests)."""
    global next_task_id
    tasks.clear()
    next_task_id = 1


def find_task(task_id: int) -> dict:
    """Return the task if it exists, otherwise raise 404."""
    if task_id not in tasks:
        raise HTTPException(status_code=404, detail="Task not found")
    return tasks[task_id]


# --- Pydantic Models ---
class TaskCreate(BaseModel):
    title: str = Field(min_length=1, max_length=120)
    description: str = ""
    completed: bool = False


class TaskReplace(BaseModel):
    title: str = Field(min_length=1, max_length=120)
    description: str
    completed: bool


class TaskRead(TaskReplace):
    id: int


# --- Routes ---
@app.post("/tasks", response_model=TaskRead, status_code=201)
def create_task(task: TaskCreate):
    global next_task_id
    saved = {"id": next_task_id, **task.model_dump()}
    tasks[next_task_id] = saved
    next_task_id += 1
    return saved


@app.get("/tasks", response_model=list[TaskRead])
def list_tasks(completed: bool | None = None):
    result = list(tasks.values())
    if completed is not None:
        result = [t for t in result if t["completed"] == completed]
    return result


@app.get("/tasks/{task_id}", response_model=TaskRead)
def get_task(task_id: int = Path(gt=0)):
    return find_task(task_id)


@app.put("/tasks/{task_id}", response_model=TaskRead)
def replace_task(task: TaskReplace, task_id: int = Path(gt=0)):
    existing = find_task(task_id)
    updated = {"id": existing["id"], **task.model_dump()}
    tasks[task_id] = updated
    return updated


@app.delete("/tasks/{task_id}", status_code=204)
def delete_task(task_id: int = Path(gt=0)):
    find_task(task_id)
    del tasks[task_id]
    return Response(status_code=204)
