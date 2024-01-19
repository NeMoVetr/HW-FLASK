from typing import List
from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()


class Task(BaseModel):
    title: str
    description: str
    status: bool = False


tasks_db = []


@app.get("/tasks", response_model=List[Task])
async def get_tasks():
    return tasks_db


@app.get("/tasks/{task_id}", response_model=Task)
async def get_task(task_id: int):
    return tasks_db[task_id]


@app.post("/tasks", response_model=List[Task])
async def create_task(task: Task):
    tasks_db.append(task)
    return tasks_db


@app.put("/tasks/{task_id}", response_model=List[Task])
async def update_task(task_id: int, new_task: Task):
    tasks_db[task_id] = new_task
    return tasks_db


@app.delete("/tasks/{task_id}", response_model=List[Task])
async def delete_task(task_id: int):
    tasks_db.pop(task_id)
    return tasks_db



