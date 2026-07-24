from typing import Optional
from fastapi import HTTPException,Response, status
from fastapi import FastAPI
from pydantic import BaseModel
from tasks import get_all_tasks, get_by_id, add_task, update_task, delete_task, get_stats, health_check
from tasks import initialize_database
from redis_client import ping_redis
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


@app.on_event("startup")
async def startup():
    initialize_database()
    if ping_redis():
        print("✅ Redis connected")
    else:
        print("❌ Redis connection failed")
@app.get("/")
async def wealth():
    return { "name": "Task API", "version": "1.0", "endpoints": ["/tasks"] }


#show health
@app.get("/health")
def health():
    if health_check():
        return {
            "status": "ok",
            "db": "ok"
        }

    return {
        "status": "error",
        "db": "failed"
    }

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
@app.post("/tasks", status_code=status.HTTP_201_CREATED)
async def add_tasks(task: newtask):
    if task.title.strip() == "":
       raise HTTPException(
    status_code=400,
    detail="Title cannot be empty"
)
    new_task = add_task(task.title,task.done)
       
    return {"New task added:" :new_task}





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
@app.delete("/tasks/{id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_tast(id : int):
    deleted = delete_task(id)
    if deleted == 0:
        raise HTTPException(
    status_code=404,
    detail="Task not found"
)

    return Response(status_code=status.HTTP_204_NO_CONTENT)


#Show statistics
@app.get("/stats")
async def get_statistics():
    return get_stats()
        



