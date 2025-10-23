from fastapi import APIRouter,Depends,HTTPException
from app.schemas.tracking_schema import TrackingCreate,TrackingResponse
from app.database import tracking_collection
from app.auth.oauth2 import get_current_user
from datetime import datetime
from bson import ObjectId

router = APIRouter(
    prefix="/tracking",
    tags = ["Tracking"]
)

@router.post("/update",response_model=TrackingResponse)
def update_location(tracking: TrackingCreate,current_user: str= Depends(get_current_user)):
    if current_user["role"]!= "driver":
        raise HTTPException(status_code=403,detail="Only drivers can update their location")

    