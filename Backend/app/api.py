# python
# file: `Backend/app/api.py`
from typing import List, Optional
from fastapi import FastAPI, HTTPException, status, Request
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

app = FastAPI()

origins = [
    "http://localhost:3000",
    "http://127.0.0.1:3000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class TodoCreate(BaseModel):
    item: str

class TodoUpdate(BaseModel):
    item: str

class TodoOut(BaseModel):
    id: str
    item: str

# in-memory store for development
todos: List[dict] = [
    {"id": "1", "item": "Read Steapen!"},
    {"id": "2", "item": "Collablat!"},
    {"id": "3", "item": "NamePower"},
    {"id": "4", "item": "BymaBeybe"},
]

@app.get("/", tags=["root"])
async def read_root() -> dict:
    return {"message": "Welcome to Task Manager API!"}

@app.get("/todo", tags=["todos"])
async def get_todos() -> dict:
    return {"data": todos}

@app.post("/todo", tags=["todos"], status_code=status.HTTP_201_CREATED)
async def add_todo(todo: TodoCreate) -> dict:
    if todos:
        next_id = str(max(int(t["id"]) for t in todos) + 1)
    else:
        next_id = "1"
    new = {"id": next_id, "item": todo.item}
    todos.append(new)
    return {"data": new}

@app.put("/todo/{id}", tags=["todos"])
async def update_todo(id: str, body: TodoUpdate, request: Request) -> dict:
    print(f"[DEBUG] PUT {request.url} body={body.dict()}")
    for t in todos:
        if t["id"] == id:
            t["item"] = body.item
            return {"data": f"Todo with id {id} has been updated!", "todo": t}
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Todo with id {id} not found")

@app.delete("/todo/{id}", tags=["todos"], status_code=status.HTTP_200_OK)
async def delete_todo(id: str, request: Request) -> dict:
    print(f"[DEBUG] DELETE {request.url}")
    for i, t in enumerate(todos):
        if t["id"] == id:
            removed = todos.pop(i)
            return {"data": f"Todo with id {id} deleted", "todo": removed}
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Todo with id {id} not found")
