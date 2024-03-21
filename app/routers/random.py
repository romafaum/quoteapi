from fastapi import FastAPI, HTTPException, Response, status, APIRouter, Depends, Query
from sqlalchemy.orm import Session
from sqlalchemy.sql.expression import text
from ..schemas import QuoteOut
from ..models import Quotes
from ..database import get_db

router = APIRouter(
    prefix='/random'
)

@router.get("/", response_model=QuoteOut)
def get_random_quote(db: Session = Depends(get_db)):
    quote = db.query(Quotes).order_by(text('RANDOM()')).first()
    return quote