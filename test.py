import csv
from sqlalchemy import delete
from sqlalchemy.exc import IntegrityError
from app.database import SessionLocal
from  app.models import Quotes, Tag

with open('/home/romafaum/quotesAPI/quotes.csv', newline='') as csvfile:

    reader = csv.DictReader(csvfile)
    a = 0
    for row in reader:
        if a < 150000:
            a += 1
            continue

        with SessionLocal.begin() as session:
            quote = session.query(Quotes).filter(Quotes.quote==row['quote']).first()
            if not quote:
                continue
            tags_row = row['category'].split(', ')
            tags_set = set()
            for tag in tags_row:
                    tag_in = session.query(Tag).filter(Tag.name==tag).first()
                    tags_set.add(tag_in)
            quote.tags.extend(tags_set)
            session.commit()