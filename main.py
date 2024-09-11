from fastapi import FastAPI, HTTPException, Depends
from sqlalchemy.orm import Session
import httpx
from database import get_db
from models import Joke
from schemas import JokeCreate, JokeResponse


from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()




# External JokeAPI URL (Fetching 100 jokes)
JOKE_API_URL = "https://v2.jokeapi.dev/joke/Any?amount=100"

@app.post("/jokes/")
async def fetch_and_store_jokes(db: Session = Depends(get_db)):
    print("hello heet shah")
    try:
        # Fetch jokes from JokeAPI
        async with httpx.AsyncClient() as client:
            response = await client.get(JOKE_API_URL)
            response.raise_for_status()  # Raise error if request failed
            jokes_data = response.json()['jokes']

        # Process and store jokes in the database
        for joke_data in jokes_data:
            joke_entry = JokeCreate(
                category=joke_data.get('category', ''),
                type=joke_data.get('type', ''),
                joke=joke_data.get('joke', None),
                setup=joke_data.get('setup', None),
                delivery=joke_data.get('delivery', None),
                nsfw=joke_data.get('flags', {}).get('nsfw', False),
                political=joke_data.get('flags', {}).get('political', False),
                sexist=joke_data.get('flags', {}).get('sexist', False),
                safe=joke_data.get('safe', False),
                lang=joke_data.get('lang', '')
            )
            store_joke_in_db(db, joke_entry)

        return {"message": "Jokes fetched and stored successfully."}

    except httpx.HTTPStatusError as e:
        print("jjjjjj")
        raise HTTPException(status_code=500, detail=f"Error fetching jokes: {e}")

    except Exception as e:
        print("lllllllll")
        print(f"General Error: {e}")
        raise HTTPException(status_code=500, detail=f"An error occurred: {e}")

# Helper function to store a joke in the database
def store_joke_in_db(db: Session, joke: JokeCreate):
    # Handle different joke types and store properly
    if joke.type == "twopart":
        joke.joke = f"{joke.setup} - {joke.delivery}"  # Combine setup and delivery for twopart jokes

    db_joke = Joke(**joke.dict())  # Unpack the joke into the Joke model
    db.add(db_joke)
    db.commit()
    db.refresh(db_joke)
    return db_joke

@app.get("/jokes/", response_model=list[JokeResponse])
def get_jokes(db: Session = Depends(get_db)):
    try:
        # Query the database for all jokes
        jokes = db.query(Joke).all()
        return jokes  # SQLAlchemy models are automatically converted to Pydantic models
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"An error occurred: {e}")
