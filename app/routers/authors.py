from typing import List
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from sqlalchemy.sql.expression import text
from .functions.authors_querys import query_author, query_sources, query_tags, author_404
from ..schemas import QuoteOut, AuthorOut, TagInfo, AuthorStats, SourceInfo
from ..models import Quotes, Author
from ..database import get_db


router = APIRouter(
    prefix='/author',
    tags=['Search']
)



@router.get("/{id}", response_model=AuthorStats)
def autor_get(id: int, db: Session = Depends(get_db)):
    author = query_author(db).filter(Author.id == id).first()
    author_404(author, id)

    tags = query_tags(db, id).all()
    sources = query_sources(db, id).all()
    author_id, author_name, total_quotes = author
    top_tags = [TagInfo(id=row[0], name=row[1], total=row[2]) for row in tags]
    result = AuthorStats(author=AuthorOut(id=author_id, fullname=author_name, total=total_quotes), top_tags=top_tags)
    if sources:
        top_sources = [SourceInfo(name=row[0], total=row[1]) for row in sources]
        result.sources = top_sources
    return result


@router.get("/{id}/random", response_model=QuoteOut)
def autor_get(id: int, db: Session = Depends(get_db)):
    quote = db.query(Quotes)\
    .filter(Quotes.author_id == id)\
    .order_by(text('RANDOM()')).first()
    author_404(quote, id)
    return quote

@router.get("/{id}/all", response_model=List[QuoteOut])
def autor_get(id: int, db: Session = Depends(get_db)):
    quote = db.query(Quotes)\
    .filter(Quotes.author_id == id).all()
    author_404(quote, id)
    return quote