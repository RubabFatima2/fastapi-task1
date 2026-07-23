
from fastapi import FastAPI
from pydantic import BaseModel
from tasks import get_all_tasks, get_by_id
class newtask(BaseModel):
    title : str
  
class changedtask(BaseModel):
    id : int
    title : str
    done : bool

app = FastAPI()

# tasks = [{"id":0, "title":"glossary", "done":True},
#         {"id":1, "title":"shopping", "done":True},
#         {"id":3, "title":"work", "done":False} ]

# reset_tasks = [{"id":0, "title":"glossary", "done":True},
#         {"id":1, "title":"shopping", "done":True},
#         {"id":3, "title":"work", "done":False} ]



@app.get("/")
async def wealth():
    return { "name": "Task API", "version": "1.0", "endpoints": ["/tasks"] }

@app.get("/health")
async def health():
    return { "status": "ok" }

# @app.get("/tasks")
# async def done_filter(done : bool | None = None, title : str | None = None):
#     done_tasks = []
#     search_tasks=[]
#     for task in tasks:
#         if task["done"] == done:
#             done_tasks.append(task)
#         if task["title"] == title:
#              search_tasks.append(task)
#     return {"Task": done_tasks, "searched_tasks": search_tasks}
    
@app.get("/tasks")
async def get_tasks():
     return get_all_tasks()


@app.get("/tasks/{id}")
async def all_list(id:int):
    
    task = get_by_id(id)
    if task is None:
        raise HTTPException(
            status_code=404,
            detail=f"Task {id} not found"
        )
    return task

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



@app.get("/stats")
async def get_stats():
    total_tasks=0
    total_done = 0
    total_undone = 0
    for task in tasks:
        total_tasks+=1
        if task["done"] == True:
            total_done+=1
        if task["done"] == False:
            total_undone+=1
    return { "total": total_tasks, "done": total_done, "open": total_undone }
        
        
@app.post("/reset")
async def get_reset():
    global tasks
    tasks = reset_tasks
    return {"reset tasks": tasks}    


