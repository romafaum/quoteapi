import csv
from sqlalchemy import delete
from app.database import SessionLocal
from app.models import Quotes, Source, Author, Tag

def delete_data():
    with SessionLocal.begin() as session:
        session.execute(delete(Quotes))
        session.execute(delete(Source))
        session.execute(delete(Author))
        session.execute(delete(Tag))
        session.commit()

def add_author(author):
     with SessionLocal.begin() as session:
        authors.add(author)
        session.add(Author(fullname=author))
        session.commit()

def add_quote(quote, author_row):
    with SessionLocal.begin() as session:
        author = session.query(Author).filter(Author.fullname == author_row).first()
        quote = Quotes(quote=quote, author_id=author.id)
        session.add(quote)
        session.commit()

def add_source(source):
    with SessionLocal.begin() as session:
        sources.add(source)
        session.add(Source(name=source))
        session.commit()

def add_source_to_quote(quote, source):
    with SessionLocal.begin() as session:
                source = session.query(Source).filter(Source.name == source).first()
                session.query(Quotes).filter(Quotes.quote==quote).update({Quotes.source_id:source.id}, synchronize_session=False)
                session.commit()

def add_tag(tags_row):
     with SessionLocal.begin() as session:
        for tag in tags_row:
            if not tag in tags:
                tags.add(tag)
                session.add(Tag(name=tag))
        session.commit()

def add_tag_to_quote(tags_row):
     with SessionLocal.begin() as session:
        quote = session.query(Quotes).filter(Quotes.quote==row['quote']).first()
        for tag in tags_row:
            try:
                quote.append(session.query(Tag).filter(Tag.name == tag).first())
            except:
                    pass
        session.commit()

tags = set()
sources = set()
authors = set()
delete_data()

with open('/home/romafaum/quotesAPI/quotes.csv', newline='') as csvfile:
    reader = csv.DictReader(csvfile)
    for row in reader:
        tags_row = row['category'].split(', ')
        second_row = row['author'].split(', ', 1)
        if len(second_row[0]) > 120:
                continue
        if not second_row[0] in authors:
            add_author(second_row[0])
        add_quote(row['quote'], second_row[0])
        if len(second_row) == 2:
            if not second_row[1] in sources:
                add_source(second_row[1])
            add_source_to_quote(row['quote'], second_row[1])
        add_tag(tags_row)
        add_tag_to_quote(tags_row)

