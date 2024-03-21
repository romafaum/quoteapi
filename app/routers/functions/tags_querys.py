from fastapi import HTTPException, status
from sqlalchemy import  and_, func, desc
from ...models import Quotes, Tag, tags_to_quotes_table, Author, Source, Tag

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