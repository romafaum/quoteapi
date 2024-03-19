import csv
from sqlalchemy import delete
from app.database import SessionLocal
from  app.models import Quotes, Tag

with open('/home/romafaum/quotesAPI/quotes.csv', newline='') as csvfile:

    reader = csv.DictReader(csvfile)
    for row in reader:
        with SessionLocal.begin() as session:
            quote = session.query(Quotes).filter(Quotes.quote==row['quote']).first()
            tags_row = row['category'].split(', ')
            for tag in tags_row:
                tag_in = session.query(Tag).filter(Tag.name==tag).first()
                quote.tags.append(tag_in)
            session.commit()