from typing import Optional, List
from fastapi import APIRouter, Depends, Query
from sqlalchemy import  and_
from sqlalchemy.orm import Session
from ..schemas import QuoteOut
from ..models import Quotes, Tag, Author, Source
from ..database import get_db


router = APIRouter(
    prefix='/search',
    tags=['Search']
)

@router.get("/", response_model=List[QuoteOut])
def search_quote(
        db: Session = Depends(get_db),
        limit: int = 10, start: int = 0, quote: Optional[str] = "",
        tags: List[str] = Query(None, split=True),
        author: Optional[str] = "",
        source: Optional[str] = ""
    ):
    quotes = db.query(Quotes).filter(Quotes.quote.contains(quote)) 
    if tags:
        quotes = quotes.filter(and_(Quotes.tags.any(Tag.name.in_([tag])) for tag in tags))
    if author:
        quotes = quotes.join(Author).filter(Author.fullname.contains(author))
    if source:
        quotes = quotes.join(Source).filter(Source.name.contains(source))
    return quotes.limit(limit).all()