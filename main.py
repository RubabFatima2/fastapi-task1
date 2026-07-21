
from fastapi import FastAPI
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

@app.get("/tasks/{id}")
async def all_list(id:int):
    for task in tasks:
        if task["id"] == id:
            return task
    return {"error": f"Task 99 has no id"}