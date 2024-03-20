from typing import List, Optional
from pydantic import BaseModel

class Author(BaseModel):
    id: int
    fullname: str

class Source(BaseModel):
    id: int
    name: str

class TagOut(BaseModel):
    name: str

class QuoteOut(BaseModel):
    id: int
    quote: str
    author: Author
    sourse: Optional[Source] = None
    tags: List[TagOut]

class TagInfo(BaseModel):
    name: str
    total: int

class AuthorOut(Author):
    total_quotes: int

class SourceInfo(BaseModel):
    name: str
    total: int

class AuthorStats(BaseModel):
    author: AuthorOut
    top_tags: List[TagInfo]
    sources: Optional[List[SourceInfo]] = None