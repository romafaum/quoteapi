from random import choice
from typing import List
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from .functions.tags_querys import query_tag, tag_404, query_authors, query_related_tags, query_sources
from ..schemas import QuoteOut, AuthorOut, TagInfo, SourceInfo, TagStats
from ..models import Tag
from ..database import get_db
router = APIRouter(
    prefix="/tags",
    tags=["Tags"]
)


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
    tag = db.query(Tag).filter(Tag.id == id).first()
    tag_404(tag, id)
    return tag.quotes

@router.get('/{id}/random', response_model=QuoteOut)
def tag_quotes(id: int, db: Session = Depends(get_db)):
    tag = db.query(Tag).filter(Tag.id == id).first()
    tag_404(tag, id)
    return choice(tag.quotes)