from typing import List, Optional
from pydantic import BaseModel

class Author(BaseModel):
    fullname: str

class Source(BaseModel):
    name: str

class Tag(BaseModel):
    name: str

class QuoteOut(BaseModel):
    id: int
    source_id: int
    quote: str
    author: Author
    sourse: Optional[Source] = None
    tags: List[Tag]
