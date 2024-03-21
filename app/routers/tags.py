from random import choice
from typing import Optional, List, Union
from fastapi import HTTPException, Response, status, APIRouter, Depends, Query
from sqlalchemy import  and_, func, desc
from sqlalchemy.orm import Session
from sqlalchemy.sql.expression import text
from ..schemas import QuoteOut, TagOut, AuthorOut, TagInfo, AuthorStats, SourceInfo, TagStats
from ..models import Quotes, Tag, tags_to_quotes_table, Author, Source, Tag
from ..database import get_db

router = APIRouter(
    prefix="/tags",
    tags=["Tags"]
)

def tag_404(tag, id):
    if not tag:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail= f"Tag with id:{id} not found"
        )

def query_tag(db):
    tag = db.query(Tag.id, Tag.name, func.count(Tag.id).label("total")) \
    .join(tags_to_quotes_table).join(Quotes).group_by(Tag.id)
    return tag

def query_authors(db, id):
    authors = db.query(Author.id, Author.fullname, func.count(Author.id).label("total_quotes"))\
    .join(Quotes)\
    .join(tags_to_quotes_table)\
    .join(Tag)\
    .filter(Tag.id == id)\
    .group_by(Author.id).order_by(desc("total_quotes")).limit(5)
    return authors

def query_sources(db, id):
    sources = db.query(Source.name, func.count(Source.id).label("total"))\
    .join(Quotes)\
    .join(tags_to_quotes_table)\
    .join(Tag)\
    .filter(Tag.id == id)\
    .group_by(Source.name).order_by(desc("total"))
    return sources

def query_related_tags(db, id):
    subquery = db.query(tags_to_quotes_table.c.quote_id) \
    .filter(tags_to_quotes_table.c.tags_id == id)
    
    tags = db.query(Tag.id, Tag.name, func.count(Tag.name).label('total')).select_from(Quotes)\
    .join(tags_to_quotes_table)\
    .join(Tag, and_(tags_to_quotes_table.c.tags_id == Tag.id, Quotes.id.in_(subquery)))\
    .group_by(Tag.id).order_by(desc('total')).offset(1)
    return tags


@router.get("/{id}", response_model=TagStats)
def tag_info(id: int, db: Session = Depends(get_db), limit: int = 5):
    if limit == 0:
        limit = None
    tag = query_tag(db).filter(Tag.id == id).first()
    tag_404(tag, id)
    authors = query_authors(db, id).limit(limit).all()
    tags = query_related_tags(db, id).limit(limit).all()
    sources = query_sources(db, id).limit(limit).all()
    top_authors = [AuthorOut(id=row[0], fullname=row[1], total=row[2]) for row in authors]
    res = TagStats(tag=TagInfo(id=tag[0], name=tag[1], total=tag[2]), authors=top_authors)
    if tags:
        top_tags = [TagInfo(id=row[0], name=row[1], total=row[2]) for row in tags]
        res.related_tags = top_tags
    if sources:
        top_sources = [SourceInfo(name=row[0], total=row[1]) for row in sources]
        res.sources = top_sources
    return res

@router.get('/{id}/all', response_model=List[QuoteOut])
def tag_quotes(id: int, db: Session = Depends(get_db)):
    tag = db.query(Tag)\
    .filter(Tag.id == id).first()
    tag_404(tag, id)
    return tag.quotes

@router.get('/{id}/random', response_model=QuoteOut)
def tag_quotes(id: int, db: Session = Depends(get_db)):
    tag = db.query(Tag)\
    .filter(Tag.id == id).first()
    tag_404(tag, id)
    return choice(tag.quotes)