from db_files.database import SessionLocal
from psycopg2.extensions import register_adapter, AsIs

def parse_records(database_records):
    """
    A helper method for converting a list of database record objects into a list of dictionaries, so they can be returned as JSON
    Param: database_records (a list of db.Model instances)
    Example: parse_records(User.query.all())
    Returns: a list of dictionaries, each corresponding to a record, like...
        [
            {"id": 1, "title": "Book 1"},
            {"id": 2, "title": "Book 2"},
            {"id": 3, "title": "Book 3"},
        ]
    """
    parsed_records = []
    for record in database_records:
        # print(record)
        parsed_record = record.__dict__
        del parsed_record["_sa_instance_state"]
        parsed_records.append(parsed_record)
    return parsed_records

# Session Dependency
def get_db():
    try:
        db = SessionLocal()
        yield db
    finally:
        db.close()

# adapt numpy_int64
# https://rehalcon.blogspot.com/2010/03/sqlalchemy-programmingerror-cant-adapt.html
def adapt_numpy_int64(numpy_int64):
    return AsIs(numpy_int64)

