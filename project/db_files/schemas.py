from typing import List, Optional

from pydantic import BaseModel

# create pydantic schema. "Pydantic guarantees that the data fields of the resultant model
# conform to the field types we define" --
#  https://towardsdatascience.com/fastapi-cloud-database-loading-with-python-1f531f1d438a
class Project(BaseModel):
    id: int
    latitude: float
    longitude: float
    district_id: int
    district_name: str
    province_id: int
    province_name: str
    project_stage: str
    individuals_served: int
    bridge_image: str

    class Config:
        orm_mode = True



