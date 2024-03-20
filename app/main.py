from typing import Optional, List
from fastapi import FastAPI, HTTPException, Response, status, APIRouter, Depends, Query
from sqlalchemy import  and_
from sqlalchemy.orm import Session
from sqlalchemy.sql.expression import text
from .schemas import QuoteOut, TagOut
from .models import Quotes, Tag, tags_to_quotes_table, Author, Source
from .database import get_db
from .routers import search, random, sources, authors, tags
 

app = FastAPI()

@app.get("/")
def root():
    return {"Message": "Hello world"}

@app.get("/random", response_model=QuoteOut)
def get_random_quote(db: Session = Depends(get_db)):
    quote = db.query(Quotes)\
    .order_by(text('RANDOM()')).limit(1).first()
    return quote

app.include_router(search.router)
app.include_router(random.router)
app.include_router(authors.router)