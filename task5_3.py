
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List

app = FastAPI()

class Task(BaseModel):
    id: int
    task: str

tasks: List[Task] = []

@app.post("/tasks", response_model=Task)
async def add_task(task: Task):
    tasks.append(task)
    return task

@app.get("/tasks", response_model=List[Task])
async def get_tasks():
    return tasks

@app.get("/tasks/{task_id}", response_model=Task)
async def get_task(task_id: int):
    for task in tasks:
        if task.id == task_id:
            return task
    raise HTTPException(status_code=404, detail="Task not found")

@app.delete("/tasks/{task_id}", response_model=Task)
async def delete_task(task_id: int):
    for task in tasks:
        if task.id == task_id:
            tasks.remove(task)
            return task
    raise HTTPException(status_code=404, detail="Task not found")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
