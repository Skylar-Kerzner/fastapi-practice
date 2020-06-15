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
"""
1. Given a search term, pull text from closest wikipedia page
2. Calculate word stats that show the zipf principle
3. Write stats to db
4. Retrieve stats from db
"""

models.Base.metadata.create_all(bind=engine)

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


# Background task in same container as API for this version. 
# Then use dramatiq to put worker in separate container in another version
def write_stats_to_db(search_term, db):
    common_words_counts, tags_counts, page_name, total_words = get_most_common_words_tags_counts(search_term)
    logger.debug(f"{common_words_counts}")
    wikistats_entry = create_wikistats_entry(common_words_counts, page_name)
    logger.debug(f"Row to add to db: {wikistats_entry.__dict__}")
    db.add(wikistats_entry)
    db.commit()
    logger.info(f"Committed {page_name} entry to db")
    return

# POST: Run task and write results to db
@app.post("/wikicounts/")
async def add_item(search: Search, background_tasks : BackgroundTasks, db: Session = Depends(get_db)):
    background_tasks.add_task(write_stats_to_db, search.term, db)
    return {"message" : f"Running analytics on wikipage closest to '{search.term}'"}



# GET: Retrieve data from db
@app.get("/wikicounts/")
async def read_items(db: Session = Depends(get_db)):
    results = db.query(Wikistats).all()
    logger.debug(f"{results}")
    return {"results" : results}


# : Delete db
@app.delete("/wikicounts/delete/")
async def delete_items(db: Session = Depends(get_db)):
    db.query(Wikistats).delete()
    db.commit()
    results = db.query(Wikistats).all()
    logger.warning(f"DELETED DATABASE")
    return {"results" : results}


