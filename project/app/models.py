from sqlalchemy import Column, ForeignKey, Integer, Float, String
from sqlalchemy.orm import relationship

from database import Base

# Create classes for each table that will be in our Database. 
class Province(Base):
    __tablename__ = 'provinces'

    id = Column(Integer, primary_key=True)
    province_name = Column(String)

    projects = relationship('Project', back_populates='province')

class District(Base):
    __tablename__ = 'districts'

    id = Column(Integer, primary_key=True)
    district_name = Column(String)
    province_id = Column(Integer, ForeignKey='provinces.id')

    projects = relationship('Project', back_populates='district')

class Project(Base):
    __tablename__ = 'bridge_project'

    id = Column(Integer, primary_key=True)
    latitude = Column(Float)
    longitude = Column(Float)
    district_id = Column(Integer, ForeignKey='districts.id')
    province_id = Column(Integer, ForeignKey='provinces.id')
    project_stage = Column(String)
    individuals_served = Column(Integer)
    bridge_image = Column(String)

    province = relationship('Province', back_populates='projects')
    district = relationship('District', back_populates='district')