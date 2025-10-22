from pydantic import BaseModel,EmailStr,Field
from datetime import datetime

class NotificationBase(BaseModel):
    user_id :str
    message :str
    type:str
    read : bool = False
    created_at : datetime = Field(default_factory=datetime.utcnow)

class NotificationCreate(NotificationBase):
    pass

class NotificationResponse(NotificationBase):
    id :str
    