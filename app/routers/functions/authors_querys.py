from fastapi import HTTPException, status
from sqlalchemy import  func, desc
from ...models import Quotes, Tag, tags_to_quotes_table, Author, Source, Tag

def query_author(db):
    author = db.query(Author.id, Author.fullname, func.count(Quotes.id).label("total"))\
    .join(Quotes, Quotes.author_id == Author.id).group_by(Author.id)
    return author

def query_tags(db, id):
    tags = db.query(Tag.id, Tag.name, func.count(Tag.id).label("total"))\
    .join(tags_to_quotes_table)\
    .join(Quotes)\
    .join(Author)\
    .filter(Author.id == id)\
    .group_by(Tag.id).order_by(desc("total")).limit(5)
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