from pydantic import BaseModel
from typing import Optional

class JokeCreate(BaseModel):
    category: str
    type: str
    joke: Optional[str] = None  # For 'single' type jokes
    setup: Optional[str] = None  # For 'twopart' type jokes
    delivery: Optional[str] = None  # For 'twopart' type jokes
    nsfw: bool
    political: bool
    sexist: bool
    safe: bool
    lang: str

# schemas.py
from pydantic import BaseModel

class JokeResponse(BaseModel):
    id: int
    category: str = None
    type: str= None
    joke: str = None  # Optional field for single-type jokes
    setup: str = None  # Optional field for two-part setup
    delivery: str = None  # Optional field for two-part delivery
    nsfw: bool
    political: bool
    sexist: bool
    safe: bool
    lang: str=None

    class Config:
        orm_mode = True  # This tells Pydantic to treat SQLAlchemy models as data
