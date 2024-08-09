
from fastapi import FastAPI, HTTPException, Depends, Query
from pydantic import BaseModel
from typing import List, Optional

app = FastAPI()

# In-memory storage for tasks
tasks = []

# Pydantic model for task
class Task(BaseModel):
    id: int
    title: str
    description: Optional[str] = None
    done: bool = False

# Dependency to manage tasks
def get_tasks() -> List[Task]:
    return tasks

def get_task_by_id(task_id: int) -> Task:
    task = next((task for task in tasks if task.id == task_id), None)
    if task is None:
        raise HTTPException(status_code=404, detail="Task not found")
    return task

@app.post("/tasks/", response_model=Task)
def create_task(task: Task, tasks: List[Task] = Depends(get_tasks)):
    if any(t.id == task.id for t in tasks):
        raise HTTPException(status_code=400, detail="Task with this ID already exists")
    tasks.append(task)
    return task

@app.get("/tasks/", response_model=List[Task])
def read_tasks(tasks: List[Task] = Depends(get_tasks)):
    return tasks

@app.get("/tasks/{task_id}", response_model=Task)
def read_task(task_id: int, task: Task = Depends(lambda: get_task_by_id(task_id))):
    return task

@app.put("/tasks/{task_id}", response_model=Task)
def update_task(task_id: int, updated_task: Task, task: Task = Depends(lambda: get_task_by_id(task_id))):
    task_index = next(i for i, t in enumerate(tasks) if t.id == task_id)
    tasks[task_index] = updated_task
    return updated_task

@app.delete("/tasks/{task_id}", response_model=Task)
def delete_task(task_id: int, task: Task = Depends(lambda: get_task_by_id(task_id))):
    tasks[:] = [t for t in tasks if t.id != task_id]
    return task

# Run the application
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
