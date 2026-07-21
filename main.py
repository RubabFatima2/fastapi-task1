
from fastapi import FastAPI
from pydantic import BaseModel

class newtask(BaseModel):
    title : str
  
app = FastAPI()

tasks = [{"id":0, "title":"glossary", "done":True},
        {"id":1, "title":"shopping", "done":True},
        {"id":3, "title":"work", "done":False} ]

@app.get("/")
async def wealth():
    return { "name": "Task API", "version": "1.0", "endpoints": ["/tasks"] }

@app.get("/health")
async def health():
    return { "status": "ok" }

@app.get("/tasks")
async def get_task():
    return {"tasks:":tasks}


@app.get("/tasks/{id}")
async def all_list(id:int):
    for task in tasks:
        if task["id"] == id:
            return task
    return {"error": f"Task {id} has no id"}

@app.post("/tasks")
async def add_tasks(task: newtask):
    next_id = max(task["id"] for task in tasks) + 1
    done = False
    new_task = { "id": next_id,"title": task.title,"done":done }
    if task.title.strip() == "":
        return {"error":201}
    else:
        tasks.append(new_task)
        return {"task" : new_task}



class changedtask(BaseModel):
    id : int
    title : str
    done : bool

@app.put("/tasks/{id}")
async def change_task(id : int,  updated_task: changedtask):
    if updated_task.title.strip() == "":
        return {"error": "Title cannot be empty"}
    for task in tasks:
        if task["id"] == id:
            task.update( title= updated_task.title,done = updated_task.done)
            return {"update_task": task}
    
    return {"unknown_id":400}


@app.delete("/tasks/{id}")
async def delete_tast(id : int):
    for task in tasks:
        if task["id"] == id:
            tasks.remove(task)
            return {"status code": 404, "tasks":task}
    return {"Error": "Task not found"}


    