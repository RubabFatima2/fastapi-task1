from typing import Optional
from fastapi import HTTPException
from fastapi import FastAPI
from pydantic import BaseModel
from tasks import get_all_tasks, get_by_id, add_task, update_task, delete_task, get_stats
class newtask(BaseModel):
    title : str
    done : bool
  
class changedtask(BaseModel):

    title : str
    done : bool

app = FastAPI()

# ==========================================
# Task Management API using FastAPI + SQLite
# Assignment 2
# ==========================================
@app.get("/")
async def wealth():
    return { "name": "Task API", "version": "1.0", "endpoints": ["/tasks"] }


#show health
@app.get("/health")
async def health():
    return { "status": "ok" }

#show all tasks
@app.get("/tasks")
async def get_tasks(search: Optional[str] = None,
    done: Optional[bool] = None):
     return get_all_tasks(search, done)


#show tasks by id
@app.get("/tasks/{id}")
async def all_list(id:int):
    
    task = get_by_id(id)
    if task is None:
        raise HTTPException(
            status_code=400,
            detail=f"Task {id} not found"
        )
    return task

#Add tasks
@app.post("/tasks")
async def add_tasks(task: newtask):
    if task.title.strip() == "":
       raise HTTPException(
    status_code=400,
    detail="Title cannot be empty"
)
    new_task = add_task(task.title,task.done)
       
    return {"Created successfully": 201, "New task added:" :new_task}





#Update tasks
@app.put("/tasks/{id}")
async def change_task(id: int, updated_task: changedtask):
    if updated_task.title.strip() == "":
        raise HTTPException(
            status_code=400,
            detail="Title cannot be empty"
        )

    u_task = update_task(id, updated_task.title, updated_task.done)

    if u_task is None:
        raise HTTPException(
            status_code=404,
            detail=f"Task {id} not found"
        )

    return {"updated_task": u_task}




#Delete task
@app.delete("/tasks/{id}")
async def delete_tast(id : int):
    deleted = delete_task(id)
    if deleted == 0:
        raise HTTPException(
    status_code=404,
    detail="Task not found"
)

    return {"Status": "Task deleted"}


#Show statistics
@app.get("/stats")
async def get_statistics():
    return get_stats()
        



