from typing import List, Optional
from sqlalchemy import ForeignKey, String, Table, Column, Text
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship

class Base(DeclarativeBase):
    pass

tags_to_quotes_table = Table(
    "tags_and_quotes",
    Base.metadata,
    Column('quote_id', ForeignKey("quotes.id", ondelete="CASCADE"), primary_key=True),
    Column('tags_id', ForeignKey("tags.id", ondelete="CASCADE"), primary_key=True)
)

class Quotes(Base):
    __tablename__ = 'quotes'

    id: Mapped[int] = mapped_column(primary_key=True)
    quote: Mapped[Text] = mapped_column(Text())
    author_id: Mapped[int] = mapped_column(ForeignKey('authors.id', ondelete="CASCADE"))
    source_id: Mapped[int | None] = mapped_column(ForeignKey('sources.id'))
    author: Mapped["Author"] = relationship(back_populates="quotes")
    sourse: Mapped[Optional["Source"]] = relationship(back_populates="quotes")
    tags: Mapped[Optional[List["Tag"]]] = relationship(secondary=tags_to_quotes_table, back_populates="quotes")


class Author(Base):
    __tablename__ = "authors"

    id: Mapped[int] = mapped_column(primary_key=True)
    fullname: Mapped[str] = mapped_column(String(300), unique=True)
    quotes: Mapped[Optional["Quotes"]] = relationship(back_populates="author")

class Source(Base):
    __tablename__ = "sources"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(800), unique=True)
    quotes: Mapped[Optional["Quotes"]] = relationship(back_populates="sourse")

class Tag(Base):
    __tablename__ = "tags"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(300), unique=True)
    quotes: Mapped[Optional[List["Quotes"]]] = relationship(secondary=tags_to_quotes_table, back_populates="tags")
