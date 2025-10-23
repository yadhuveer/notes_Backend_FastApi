from fastapi import APIRouter, HTTPException, status
from app import dataTypes
from app.utils.hashing import hash_password, verify_password
from app.Authentication.authentication import create_access_token
from app.Mongo_Connection import  get_database
from app.requiredData import get_user_doc


router = APIRouter(prefix="/user", tags=["User"])


@router.post("/signup", response_model=dataTypes.UserResponse)
async def create_user(request: dataTypes.UserCreate):
    db=get_database()
    existing_user = await db["users"].find_one({"user_email": request.user_email})
    if existing_user:
        raise HTTPException(status_code=400, detail="Email already registered")

    hashed_pw = hash_password(request.password)
    new_user = get_user_doc(request.user_name, request.user_email, hashed_pw)
    await db["users"].insert_one(new_user)

    return {
        "user_id": new_user["_id"],
        "user_name": new_user["user_name"],
        "user_email": new_user["user_email"],
        "created_on": new_user["created_on"],
    }


@router.post("/login", response_model=dataTypes.Token)
async def login_user(request: dataTypes.UserLogin):
    db=get_database()
    user = await db["users"].find_one({"user_email": request.user_email})
    if not user or not verify_password(request.password, user["password"]):
        raise HTTPException(status_code=404, detail="Invalid email or password")

    
    
    access_token = create_access_token(user["_id"])
    return {"access_token": access_token, "token_type": "bearer"}
