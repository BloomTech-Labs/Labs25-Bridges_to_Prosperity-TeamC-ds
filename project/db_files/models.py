from sqlalchemy import Column, ForeignKey, Integer, Float, String
from sqlalchemy.orm import relationship

from db_files.database import Base

# Create classes for each table that will be in our Database. 
class Project(Base):
    __tablename__ = 'bridge_project'

    id = Column(Integer, primary_key=True)
    latitude = Column(Float)
    longitude = Column(Float)
    district_id = Column(Integer, ForeignKey('districts.id'))
    district_name = Column(String)
    province_id = Column(Integer, ForeignKey('provinces.id'))
    province_name = Column(String)
    project_stage = Column(String)
    individuals_served = Column(Integer)
    bridge_image = Column(String)