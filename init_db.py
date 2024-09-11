from database import Base, engine
from models import Joke

# Create tables in the database
Base.metadata.create_all(bind=engine)
