from typing import Optional, List, Union
from fastapi import HTTPException, Response, status, APIRouter, Depends, Query
from sqlalchemy import  and_, func, desc
from sqlalchemy.orm import Session
from sqlalchemy.sql.expression import text
from ..schemas import QuoteOut, TagOut, AuthorOut, TagInfo, AuthorStats, SourceInfo
from ..models import Quotes, Tag, tags_to_quotes_table, Author, Source, Tag
from ..database import get_db


router = APIRouter(
    prefix='/author',
    tags=['Search']
)

def query_author(db):
    author = db.query(Author.id, Author.fullname, func.count(Quotes.id).label("total"))\
    .join(Quotes, Quotes.author_id == Author.id).group_by(Author.id)
    return author

def query_tags(db, id):
    tags = db.query(Tag.name, func.count(Tag.id).label("total"))\
    .join(tags_to_quotes_table)\
    .join(Quotes)\
    .join(Author)\
    .filter(Author.id == id)\
    .group_by(Tag.name).order_by(desc("total")).limit(5)
    return tags

def query_sources(db, id):
    tags = db.query(Source.name, func.count(Source.id).label("total"))\
    .join(Quotes)\
    .join(Author)\
    .filter(Author.id == id)\
    .group_by(Source.name).order_by(desc("total"))
    return tags

def author_404(author, id):
    if not author:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail= f"Author with id:{id} not found"
        )

@router.get("/{id}", response_model=AuthorStats)
def autor_get(id: int, db: Session = Depends(get_db)):
    author = query_author(db).filter(Author.id == id).first()
    author_404(author, id)

    tags = query_tags(db, id).all()
    sources = query_sources(db, id).all()
    author_id, author_name, total_quotes = author
    top_tags = [TagInfo(name=row[0], total=row[1]) for row in tags]
    result = AuthorStats(author=AuthorOut(id=author_id, fullname=author_name, total_quotes=total_quotes), top_tags=top_tags)
    if sources:
        top_souces = [SourceInfo(name=row[0], total=row[1]) for row in sources]
        result.sources = top_souces
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