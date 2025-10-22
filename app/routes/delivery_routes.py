from fastapi import APIRouter,Depends,HTTPException,status
from typing import List
from app.schemas.delivery_schema import DeliveryCreate,DeliveryResponse,DeliveryUpdate
from app.database import deliveries_collection,db
from bson import ObjectId
from app.auth.oauth2 import get_current_user
from datetime import datetime
router = APIRouter(
    prefix = "/deliveries",
    tags = ["Deliveries"]
)

@router.post("/create",response_model=DeliveryResponse)
def create_delivery(delivery: DeliveryCreate,current_user: str = Depends(get_current_user)):
    if current_user["role"] != "customer":
        raise HTTPException(status_code=403,detail="Only customers can create deliveries")
    delivery_dict = delivery.model_dump()
    delivery_dict["customer_id"] = str(current_user["id"])
    delivery_dict["status"] = "pending"
    delivery_dict["created_at"] = datetime.utcnow()
    res = deliveries_collection.insert_one(delivery_dict)
    return DeliveryResponse(id=str(res.inserted_id),**delivery_dict)

@router.get("/",response_model=List[DeliveryResponse])
def get_all_deliveries(current_user: str = Depends(get_current_user)):
    if current_user["role"]!="admin":
        raise HTTPException(status_code=403,detail="Only admins can view all deliveries")
    deliveries=[]
    for delivery in deliveries_collection.find():
        deliveries.append(DeliveryResponse(id=str(delivery["_id"]),**delivery))
    return deliveries

@router.get("/my",response_model=DeliveryResponse)
def get_my_deliveries(current_user: str = Depends(get_current_user)):
    if current_user["role"]=="customer":
        query = {"customer_id": str(current_user["id"])}
    elif current_user["role"]=="driver":
        query = {"driver_id": str(current_user["id"])}
    else:
        raise HTTPException(status_code=403,detail="Only customers and drivers can view their deliveries")
    deliveries=[]
    for delivery in deliveries_collection.find(query):
        deliveries.append(DeliveryResponse(id=str(delivery["_id"]),**delivery))
    return deliveries

@router.put("/assign/{delivery_id}", response_model=DeliveryResponse)
def assign_driver(delivery_id: str, driver_id: str, current_user: dict = Depends(get_current_user)):
    if current_user["role"] != "admin":
        raise HTTPException(status_code=403, detail="Only admins can assign drivers")

    delivery = deliveries_collection.find_one({"_id": ObjectId(delivery_id)})
    if not delivery:
        raise HTTPException(status_code=404, detail="Delivery not found")

    deliveries_collection.update_one(
        {"_id": ObjectId(delivery_id)},
        {"$set": {"driver_id": driver_id, "status": "assigned"}}
    )
    delivery = deliveries_collection.find_one({"_id": ObjectId(delivery_id)})
    delivery["id"] = str(delivery["_id"])
    return DeliveryResponse(**delivery)

@router.put("/status/{delivery_id}",response_model=DeliveryResponse)
def update_delivery_status(delivery_id:str,update:DeliveryUpdate,current_user: dict = Depends(get_current_user)):
    if current_user["role"] != "driver":
        raise HTTPException(status_code=403, detail="Only drivers can update delivery status")
    delivery = deliveries_collection.find_one({"_id": ObjectId(delivery_id)})

    if not delivery:
        raise HTTPException(status_code=404,detail="Delivery not found")
    if delivery.get("driver_id")!= str(current_user["_id"]):
        raise HTTPException(status_code=403,detail="You are not assigned to this delivery")
    deliveries_collection.update_one(
        {"_id": ObjectId(delivery_id)},
        {"$set": {"status": update.status, "updated_at": datetime.utcnow()}}
    )
    delivery = deliveries_collection.find_one({"_id": ObjectId(delivery_id)})
    delivery["id"] = str(delivery["_id"])
    return DeliveryResponse(**delivery)