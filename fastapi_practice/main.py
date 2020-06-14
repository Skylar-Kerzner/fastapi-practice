from fastapi import FastAPI, Query
from typing import List

app = FastAPI()


@app.get("/")
def read_root():
    return {"Hello": "World"}


@app.get("/inputs/{item_id}")
def read_item(item_id: str, q: List[str] = Query(None)): # List[str] = Query(None)
    return {"item_id": item_id, "q": q}