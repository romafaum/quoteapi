from typing import List, Optional
from pydantic import BaseModel

class Author(BaseModel):
    fullname: str

class Source(BaseModel):
    name: str

class TagOut(BaseModel):
    name: str

class QuoteOut(BaseModel):
    id: int
    quote: str
    author: Author
    sourse: Optional[Source] = None
    tags: List[TagOut]
