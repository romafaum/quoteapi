from typing import List, Optional
from sqlalchemy import ForeignKey, String, Table, Column
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship

class Base(DeclarativeBase):
    pass

tags_to_quotes_table = Table(
    "tagsandquotes",
    Base.metadata,
    Column('quote_id', ForeignKey("quotes.id"), primary_key=True),
    Column('author_id', ForeignKey("authors.id"), primary_key=True)
)

class Quotes(Base):
    __tablename__ = 'quotes'

    id: Mapped[int] = mapped_column(primary_key=True)
    author_id: Mapped[int] = mapped_column(ForeignKey('authors.id', ondelete="CASCADE"))
    source_id: Mapped[int | None] = mapped_column(ForeignKey('authors.id'))
    author: Mapped["Author"] = relationship(back_populates="quotes")
    sourse: Mapped["Source" | None] = relationship(back_populates="quotes")
    tags: Mapped[List["Tag"]] = relationship(secondary=tags_to_quotes_table, back_populates="quotes")


class Author(Base):
    __tablename__ = "authors"

    id: Mapped[int] = mapped_column(primary_key=True)
    fullname: Mapped[str] = mapped_column(String(80))

class Source(Base):
    __tablename__ = "sources"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(250))

class Tag(Base):
    __tablename__ = "tags"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(300))
