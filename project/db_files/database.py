import os
from dotenv import load_dotenv

load_dotenv()

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# this was created using modified steps from Fastapi tutorial on SQL relational 
# Databases. https://fastapi.tiangolo.com/tutorial/sql-databases/

# get the database url from env file

# environment variables for DB login
DIALECT = os.getenv('DIALECT')
RDS_DB_NAME = os.getenv('RDS_DB_NAME')
RDS_USER_NAME = os.getenv('RDS_USER_NAME')
RDS_PASSWORD = os.getenv('RDS_PASSWORD')
RDS_HOST_NAME = os.getenv('RDS_HOST_NAME')
RDS_PORT = os.getenv('RDS_PORT')

# URL for engine creation using SQL ALCHEMY
#  dialect+driver://username:password@host/database
DATABASE_URL = f'{DIALECT}://{RDS_USER_NAME}:{RDS_PASSWORD}@{RDS_HOST_NAME}/{RDS_DB_NAME}'

# create engine to connect to AWS RDS instance
engine = create_engine(DATABASE_URL)

# create session for SessionLocal class. 
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# create a base class. This will return a class that we will use later to 
# create each of the database models or classes.
Base = declarative_base()
