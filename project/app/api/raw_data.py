from fastapi import APIRouter, HTTPException, Depends
from app.main import get_db
from db_files import models, schemas
from typing import List
import json



router = APIRouter()

@router.get("/projects/", response_model=List[schemas.Project])
async def show_records(db: Session = Depends(get_db)):
    '''
    uses database dependency function from main.py.
    opens a new session to the database.
    runs queries database for all data and returns as json
    closes database connection.
    
    '''
    projects = db.query(models.Project).all()
    return json.dumps([dict(project) for project in projects])
    # return projects