from typing import List, Optional
from pydantic import BaseModel

class Author(BaseModel):
    id: int
    fullname: str

class Source(BaseModel):
    id: int
    name: str

class TagOut(BaseModel):
    id: int
    name: str

class QuoteOut(BaseModel):
    id: int
    quote: str
    author: Author
    sourse: Optional[Source] = None
    tags: List[TagOut]

class TagInfo(TagOut):
    total: int

class AuthorOut(Author):
    total: int

class SourceInfo(BaseModel):
    name: str
    total: int

class AuthorStats(BaseModel):
    author: AuthorOut
    top_tags: List[TagInfo]
    sources: Optional[List[SourceInfo]] = None

class TagStats(BaseModel):
    tag: TagInfo
    related_tags: Optional[List[TagInfo]] = None
    authors: List[AuthorOut]
    sources: Optional[List[SourceInfo]] = None

