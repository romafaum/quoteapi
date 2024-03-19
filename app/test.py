import csv
from sqlalchemy import delete
from database import SessionLocal
import models

session = SessionLocal()

# Delete all quotes (consider cascading deletes if needed)
session.execute(delete(models.Quotes))


# Delete all sources
session.execute(delete(models.Source))

# Delete all authors
session.execute(delete(models.Author))

# Delete all tags
session.execute(delete(models.Tag))

# Commit changes to the database
session.commit()

# Close session (optional but recommended)
session.close()

tags = set()
sources = set()
authors = set()

with open('/home/romafaum/quotesAPI/quotes.csv', newline='') as csvfile:

    reader = csv.DictReader(csvfile)
    a = 0
    for row in reader:
        tags_row = row['category'].split(', ')
        second_row = row['author'].split(', ', 1)
        if len(second_row[0]) > 120:
                continue
        with SessionLocal.begin() as session:
            if not second_row[0] in authors:
                    authors.add(second_row[0])
                    session.add(models.Author(fullname=second_row[0]))
                    session.commit()
        with SessionLocal.begin() as session:
            author = session.query(models.Author).filter(models.Author.fullname == second_row[0]).first()
            quote = models.Quotes(quote=row['quote'], author_id=author.id)
            session.add(quote)
            session.commit()
        if len(second_row) == 2:
            if not second_row[1] in sources:
                with SessionLocal.begin() as session:
                    sources.add(second_row[1])
                    session.add(models.Source(name=second_row[1]))
                    session.commit()
            with SessionLocal.begin() as session:
                source = session.query(models.Source).filter(models.Source.name == second_row[1]).first()
                session.query(models.Quotes).filter(models.Quotes.quote==row['quote']).update({models.Quotes.source_id:source.id}, synchronize_session=False)
                session.commit()
        with SessionLocal.begin() as session:
            for tag in tags_row:
                if not tag in tags:
                    tags.add(tag)
                    session.add(models.Tag(name=tag))
            session.commit()
        with SessionLocal.begin() as session:
            quote = session.query(models.Quotes).filter(models.Quotes.quote==row['quote']).first()
            for tag in tags_row:
                try:
                    quote.append(session.query(models.Tag).filter(models.Tag.name == tag).first())
                except:
                     ...
            session.commit()

print("OVER")
