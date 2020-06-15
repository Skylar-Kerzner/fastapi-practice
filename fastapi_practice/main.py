import models
from fastapi import FastAPI, Query, BackgroundTasks, Depends
from typing import List
from pydantic import BaseModel
from nlp import get_most_common_words_tags_counts
from models import Wikistats
from sqlalchemy.orm import Session
from database import SessionLocal, engine
from helpers import create_wikistats_entry
import logging

app = FastAPI()

models.Base.metadata.create_all(bind=engine)
# Background task in same container as API for this version. 
# Then use dramatiq to put worker in separate container in another version
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

class Search(BaseModel):
   term: str 

def get_db():
    try:
        db = SessionLocal()
        yield db
    finally:
        db.close()

# Write stats to the db that show the zipf principle
def write_stats_to_db(search_term, db):
    common_words_counts, tags_counts, page_name, total_words = get_most_common_words_tags_counts(search_term)
    logger.debug(f"{common_words_counts}")
    wikistats_entry = create_wikistats_entry(common_words_counts, page_name)
    logger.debug(f"Row to add to db: {wikistats_entry.__dict__}")
    db.add(wikistats_entry)
    db.commit()
    logger.info(f"Committed {page_name} entry to db")
    return

@app.post("/wikicounts/")
async def read_item(search: Search, background_tasks : BackgroundTasks, db: Session = Depends(get_db)):
    background_tasks.add_task(write_stats_to_db, search.term, db)
    return {"message" : f"Running analytics on wikipage closest to '{search.term}'"}



# The get
@app.get("/wikicounts/")
async def read_item(db: Session = Depends(get_db)):
    results = db.query(Wikistats).all()
    logger.debug(f"{results}")
    return {"results" : results}


# Trivial practice endpoints
@app.get("/")
def read_root():
    return {"Hello": {
                "one" : "World",
                "two" : "worlds"
                    }
            }

@app.get("/inputs/{item_id}")
def read_item(item_id: str, q: List[str] = Query(None)): # List[str] = Query(None)
    return {"item_id": item_id, "q": q}