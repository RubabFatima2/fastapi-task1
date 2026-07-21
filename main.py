
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
    return {"error": f"Task 99 has no id"}

@app.post("/tasks")
async def add_tasks(task: newtask):
    next_id = max(task["id"] for task in tasks) + 1
    done = False
    new_task = { "id": next_id,"title": task.title,"done":done }
    if task.title.strip() == "":
        return {"error":404}
    else:
        tasks.append(new_task)
        return {"task" : new_task}
    