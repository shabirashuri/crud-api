from fastapi import APIRouter, HTTPException, Depends, status
from typing import Annotated
from sqlalchemy.orm import Session
import models
from schema import User , User_update
from database import Sessionlocal
from password_utils import hash_password

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


@router.post("/", status_code=status.HTTP_201_CREATED)
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

    return {
        "msg": "User created successfully",
        "user": {
            "id": db_user.id,
            "firstname": db_user.firstname,
            "lastname": db_user.lastname,
            "email": db_user.email,
        },
    }


@router.get("/{user_id}", status_code=status.HTTP_200_OK)
async def get_user(user_id: int, db: db_dependency):
    user = db.query(models.User).filter(models.User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user


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
