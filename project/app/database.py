import os
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# this was created using modified steps from Fastapi tutorial on SQL relational 
# Databases. https://fastapi.tiangolo.com/tutorial/sql-databases/

# get the database url from env file
SQLALCHEMY_DATABASE_URL = os.getenv("DATABASE_URL")

# create engine to connect to AWS RDS instance
engine = create_engine(SQLALCHEMY_DATABASE_URL)

# create session for SessionLocal class. 
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# create a base class. This will return a class that we will use later to 
# create each of the database models or classes.
Base = declarative_base()