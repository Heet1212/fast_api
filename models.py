from sqlalchemy import Column, Integer, String, Boolean
from database import Base

class Joke(Base):
    __tablename__ = "jokes"

    id = Column(Integer, primary_key=True, index=True)
    category = Column(String,nullable=True)
    type = Column(String,nullable=True)
    joke = Column(String, nullable=True)
    setup = Column(String, nullable=True)
    delivery = Column(String, nullable=True)
    nsfw = Column(Boolean)
    political = Column(Boolean)
    sexist = Column(Boolean)
    safe = Column(Boolean)
    lang = Column(String,nullable=True)


