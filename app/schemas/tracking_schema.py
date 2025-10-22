from pydantic import BaseModel,Field
from datetime import datetime

class TrackingBase(BaseModel):
    delivery_id : str
    driver_id :str
    lat : float
    lng : float
    speed : float
    timestamp : datetime = Field(default_factory=datetime.utcnow)

class TrackingCreate(TrackingBase):
    pass

class TrackingResponse(TrackingBase):
    id : str
    