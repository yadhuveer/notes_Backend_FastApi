from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app import Tables, dataTypes
from app.SQL_Connection import get_db
from app.utils.hashing import hash_password, verify_password
from app.Authentication.authentication import create_access_token
from datetime import timedelta

router = APIRouter(
    prefix="/user",
    tags=["User"]
)


@router.post("/signup", response_model=dataTypes.UserResponse)
def create_user(request: dataTypes.UserCreate, db: Session = Depends(get_db)):
    existing_user = db.query(Tables.User).filter(Tables.User.user_email == request.user_email).first()
    
    if existing_user:
        raise HTTPException(status_code=400, detail="Email already registered")

    hashed_pw = hash_password(request.password)
    new_user = Tables.User(
        user_name=request.user_name,
        user_email=request.user_email,
        password=hashed_pw
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user






@router.post("/login", response_model=dataTypes.Token)
def login_user(request: dataTypes.UserLogin, db: Session = Depends(get_db)):
    user = db.query(Tables.User).filter(Tables.User.user_email == request.user_email).first()
    if not user:
        raise HTTPException(status_code=404, detail="Invalid email or password")

    if not verify_password( request.password,user.password):
        raise HTTPException(status_code=404, detail="Invalid email or password")

    
    access_token = create_access_token(user.user_id)
    return {"access_token": access_token, "token_type": "bearer"}
