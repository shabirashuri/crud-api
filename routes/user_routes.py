from fastapi import APIRouter, HTTPException, Depends, status,Request
from typing import Annotated
from sqlalchemy.orm import Session
import models
from schema import User , User_update ,login ,TokenRefreshRequest
from database import Sessionlocal
from utils.password_utils import verify_password ,hash_password
from utils.jwt_utils import create_access_token , create_refresh_token , decode_refresh_token

router = APIRouter()

# Dependency
def get_db():
    db = Sessionlocal()
    try:   
        yield db
    finally:
        db.close()

db_dependency = Annotated[Session, Depends(get_db)]


@router.get("/", status_code=status.HTTP_200_OK)
async def get_users(db: db_dependency):
    users = db.query(models.User).all()
    return users


@router.post("/register", status_code=status.HTTP_201_CREATED)
async def create_user(user: User, db: db_dependency):
    db_user = models.User(**user.dict())
    user_exists = db.query(models.User).filter(models.User.email == db_user.email).first()
    if user_exists:
        raise HTTPException(status_code=400, detail="User already exists!")
    
    if user.email is None:
        raise HTTPException(status_code=422 , detail = "email is required!")
    
    if user.password is None:
        raise HTTPException(status_code = 422, detail = "password is required!")

    db_user.password = hash_password(db_user.password)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    print(db_user)
    print(type(db_user))


    return {
        "msg": "User created successfully",
        "user": {
            "id": db_user.id,
            "firstname": db_user.firstname,
            "lastname": db_user.lastname,
            "email": db_user.email
        },
    }



@router.post("/login")
def login_user(login_data: login, db: db_dependency):
    user = db.query(models.User).filter(models.User.email == login_data.email).first()
    if not user:
        raise HTTPException(status_code=401, detail="Invalid email")

    if not verify_password(login_data.password, user.password):  # ← bcrypt check
        raise HTTPException(status_code=401, detail="Invalid password")

    # Create token
    
    access_token = create_access_token( {"id" : user.id } , user.email)
    refresh_token = create_refresh_token( {"id" : user.id } , user.email)

    return {"loged in as":user.firstname,
            "access_token": access_token, 
            "reefresh_token" : refresh_token,
            "token_type": "bearer"}




# @router.get("/{user_id}", status_code=status.HTTP_200_OK)
# async def get_user(user_id: int, db: db_dependency):
#     user = db.query(models.User).filter(models.User.id == user_id).first()
#     if not user:
#         raise HTTPException(status_code=404, detail="User not found")
#     return user



@router.get("/me")
def get_current_user(request: Request, db: db_dependency):
    user_data = request.state.user
    user = db.query(models.User).filter(models.User.id == user_data["id"]).first()
    return user




@router.post("/refresh", status_code=status.HTTP_200_OK)
def refresh_access_token(request: TokenRefreshRequest):
    refresh_token = request.refresh_token

    payload = decode_refresh_token(refresh_token)

    if not payload:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired refresh token"
        )

    user_id = payload.get("id")
    email = payload.get("email")

    if not user_id or not email:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid refresh token payload"
        )

    new_access_token = create_access_token({"id": user_id}, email)

    return {
        "new_access_token": new_access_token,
        "token_type": "bearer"
    }



@router.delete("/{user_id}", status_code=status.HTTP_200_OK)
async def delete_user(user_id: int, db: db_dependency):
    user = db.query(models.User).filter(models.User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    db.delete(user)
    db.commit()
    return {"msg": "User deleted successfully"}


@router.put("/{user_id}", status_code=status.HTTP_200_OK)
async def update_user(user_id: int, updated_user: User_update, db: db_dependency):
    user = db.query(models.User).filter(models.User.id == user_id).first()

    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    # Update only provided fields (ignore None)
    if updated_user.firstname is not None:
        user.firstname = updated_user.firstname
    if updated_user.lastname is not None:
        user.lastname = updated_user.lastname
    if updated_user.email is not None:
        user.email = updated_user.email
    if updated_user.password is not None:
        user.password = hash_password(updated_user.password) 

    db.commit()
    db.refresh(user)
    return {"msg": "User updated successfully", "user": user}
