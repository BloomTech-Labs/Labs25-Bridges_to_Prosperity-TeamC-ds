from fastapi import APIRouter, HTTPException, Depends
from db_files.database import SessionLocal, engine
from db_files import models, schemas
from typing import List
from sqlalchemy.orm import Session
import pandas as pd
import json
import numpy
from app.helpers import parse_records, get_db, register_adapter

router = APIRouter()

@router.get("/projects", response_model=List[schemas.Project])
async def show_records(db: Session = Depends(get_db)):
    '''
    Query the Projects table and returns all records
    as a list of dictionaries.
    
    '''
    projects = db.query(models.Project).all()
    return parse_records(projects)

@router.get('/db-refresh')
async def refresh(csv_file='https://raw.githubusercontent.com/Lambda-School-Labs/Labs25-Bridges_to_Prosperity-TeamC-ds/main/final_csv/final.csv'):

    '''
    drops all tables from current database; creates all tables; and populates tables with the 
    final cleaned data values received from Bridge to Prosperity
    '''
    register_adapter(numpy.int64, adapt_numpy_int64)

    # connect to the current session of database.
    db = SessionLocal()

    # # drop all tables and data and recreate the tables
    models.Base.metadata.drop_all(bind=engine)
    models.Base.metadata.create_all(bind=engine)

    # csv_url: 'https://raw.githubusercontent.com/Lambda-School-Labs/Labs25-Bridges_to_Prosperity-TeamC-ds/main/final_csv/final.csv'
    # read csv to pandas dataframe
    df = pd.read_csv(csv_file)

    # there are longitude and latitude that have 'unknown' as values. update those to be 0
    df[[' GPS (Latitude)', 'GPS (Longitude)', 'Individuals Directly Served']] = df[[' GPS (Latitude)', 'GPS (Longitude)', 'Individuals Directly Served']].replace('Unknown', 0.0)

    # update the types to match the database column field types.
    df[['Province', 'District', 'Bridge Site Name', 'Project Stage', 'Bridge Type']] = df[['Province', 'District', 'Bridge Site Name', 'Project Stage', 'Bridge Type']].astype(str)
    df[[' GPS (Latitude)', 'GPS (Longitude)']] = df[[' GPS (Latitude)', 'GPS (Longitude)']].astype(float)
    df['Individuals Directly Served'] = df['Individuals Directly Served'].astype(float).astype(int)
    df[['Project Code', 'Prov_ID', 'District_ID']] = df[['Project Code', 'Prov_ID', 'District_ID']].astype(int)

    # drop the columns that will not be added to the database table, and get rid of duplicate project codes. 
    # we only want one instance for each bridge (project code), since we arent adding the communities served to the database in this itteration.
    df = df.drop(columns=['Original_Community_col', 'Community_Served', 'Cell', 'Form: Form Name', 'Assessment Date', 'Cell_ID', 'Sector', 'Sector_ID']).drop_duplicates(subset='Project Code')
   
        
    # itterate over the dataframe and for each row create a new db record. Add each db record to the table, and then commit and close the db connection.
    for i in df.index:
        db_record = models.Project(
            id = i,
            project_code = df.iloc[i]['Project Code'],
            bridge_name = df.iloc[i]['Bridge Site Name'],
            bridge_type = df.iloc[i]['Bridge Type'],
            latitude = df.iloc[i][' GPS (Latitude)'],
            longitude = df.iloc[i]['GPS (Longitude)'],
            district_id = df.iloc[i]['District_ID'],
            district_name = df.iloc[i]['District'],
            province_id = df.iloc[i]['Prov_ID'],
            province_name = df.iloc[i]['Province'],
            project_stage = df.iloc[i]['Project Stage'],
            bridge_image = 'Waiting on Data',
            individuals_served = df.iloc[i]['Individuals Directly Served']
            )
            # add the record to table
        db.add(db_record)
    # commit all records to tables
    db.commit()
    # close the connection to database.
    db.close()

    return "Database has been refreshed"