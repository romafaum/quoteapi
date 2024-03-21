from fastapi import FastAPI
from .routers import search, random, authors, tags

app = FastAPI()

@app.get("/")
def root():
    return {"Message": "Hello world"}

app.include_router(search.router)
app.include_router(random.router)
app.include_router(authors.router)
app.include_router(tags.router)