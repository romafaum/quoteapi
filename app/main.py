from fastapi import FastAPI, HTTPException, Response, status, APIRouter, Depends
from sqlalchemy.orm import Session
from sqlalchemy.sql.expression import text
from .schemas import QuoteOut
from .models import Quotes, Tag, tags_to_quotes_table
from .database import get_db
 

app = FastAPI()

@app.get("/")
def root():
    return {"Message": "Hello world"}

@app.get("/random", response_model=QuoteOut)
def get_random_quote(db: Session = Depends(get_db)):
    result = db.query(Quotes)\
    .filter(Quotes.id == 174989).first()
    print(result.sourse)
    # .order_by(text('RANDOM()')).limit(1).first()
    # quote = db.query(Quotes).options(db.query(Tag).join(tags_to_quotes_table)).filter(Quotes.id == 17610).limit(1).first()
    return result
