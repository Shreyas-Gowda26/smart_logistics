from pydantic import BaseModel,EmailStr,Field
from datetime import datetime
from typing import Optional


class Location(BaseModel):
    lat : float
    lng : float
    address : str

class PackageDetails(BaseModel):
    weight : Optional[float]
    description : Optional[str]

class DeliveryBase(BaseModel):
    pickup_location: Location
    drop_location: Location
    package_details : Optional[PackageDetails]
    status : str = "pending"
    created_at = datetime = Field(default_factory=datetime.utcnow)

class DeliveryCreate(DeliveryBase):
    customer_id : str

class DeliveryResponse(DeliveryBase):
    id : str
    customer_id : str
    driver_id : str

class DeliveryUpdate(BaseModel):
    status : str
    updated_at : datetime = Field(default_factory=datetime.utcnow)