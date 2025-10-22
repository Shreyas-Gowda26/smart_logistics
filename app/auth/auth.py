from fastapi import APIRouter, HTTPException, status,Depends
from fastapi.security import OAuth2PasswordRequestForm
from datetime import timedelta
from app.database import users_collection,db
from app.hashing import verify_password,hash_password
from app.auth import token
from app.schemas.user_schema import UserResponse,UserCreate

router = APIRouter(prefix="/auth", tags=["AUTH"])

@router.post("/register", response_model=UserResponse)
def register_user(user: UserCreate):
    existing_user = db.users.find_one({"email": user.email})
    if existing_user:
        raise HTTPException(status_code=400, detail="Email already registered")

    user_dict = user.dict()
    user_dict["password"] = hash_password(user.password)

    result = db.users.insert_one(user_dict)
    return UserResponse(id=str(result.inserted_id), **user_dict)

@router.post("/login")
def login(user_credentials: OAuth2PasswordRequestForm = Depends()):
    # Since form sends 'username', treat it as 'email'
    user = users_collection.find_one({"email": user_credentials.username})
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email or password"
        )

    if not verify_password(user_credentials.password, user["password"]):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email or password"
        )

    access_token_expires = timedelta(minutes=token.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = token.create_access_token(
        data={"sub": str(user["_id"])},
        #expires_delta=access_token_expires
    )

    return {
        "access_token": access_token,
        "token_type": "bearer",
        "user": UserResponse(
            id=str(user["_id"]),
            username=user["username"],
            email=user["email"]
        )
    }