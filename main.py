from fastapi import FastAPI ,HTTPException,Depends,status 
from database import Sessionlocal,engine
from typing import Annotated
import models
from sqlalchemy.orm import Session # type: ignore
import json
import  bcrypt


from pydantic import  BaseModel 
from schema import User,Post


app = FastAPI()

models.Base.metadata.create_all(bind = engine)


def get_db():
    db = Sessionlocal()
    try:
        yield  db
    finally:
        db.close()

db_dependency = Annotated[Session, Depends(get_db)]





def hash_password(password : str) -> str:

    salt  =  bcrypt.gensalt()

    hashed = bcrypt.hashpw(password.encode('utf-8'), salt)

    # Convert bytes to string for database storage
    return hashed.decode('utf-8') 

def verify_password(plain_password: str, hashed_password: str) -> bool:
    """
    Compare a plain password with its hashed version.
    Returns True if they match, otherwise False.
    """
    return bcrypt.checkpw(plain_password.encode('utf-8'), hashed_password.encode('utf-8'))


# print(verify_password("123q", "$2b$12$UN/0WmwHCHu1e/9SHZjzr.2VVlIJXgG3dUZHQx3VkA7uM6Mu9.3M."))

@app.get("/user/",status_code = status.HTTP_200_OK)
async def get_users(db : db_dependency):
    users = db.query(models.User).all()
    return users
    



@app.post("/user/",status_code = status.HTTP_201_CREATED)
async def create_user(user : User , db : db_dependency): # type: ignore
    db_user = models.User(**user.dict())
    user = db.query(models.User).filter(models.User.email == db_user.email).first()
    if user:
        
        raise HTTPException(status_code = 404 , detail = "user  exist")

    print(db_user)
    password  = hash_password(db_user.password)

    print(password)
    db_user.password = password



    
    db.add(db_user)
    db.commit()

    return {"msg": "user data inserted.",
            "user" : {"id" : db_user.id,
                      "firstname" : db_user.firstname,
                      "lastname" : db_user.lastname,
                      "email" : db_user.email,
                      "password" : db_user.password
                      }}


@app.get("/user/{user_id}",status_code = status.HTTP_200_OK)
async def get_user(user_id : int , db : db_dependency): # type: ignore
    user = db.query(models.User).filter(models.User.id == user_id).first()
    if user is None:
        raise HTTPException(status_code = 404,detail = "user not found")
    return user

@app.delete("/user/{user_id}",status_code = status.HTTP_200_OK)
async def delete_user(user_id:int , db : db_dependency): # type: ignore
    user = db.query(models.User).filter(models.User.id == user_id).first()
    if user is None:
        raise HTTPException(status_code = 404 , detail = "user not found")
    db.delete(user)
    db.commit()
    return user

@app.put("/user/{user_id}", status_code=status.HTTP_200_OK)
async def update_user(user_id: int, updated_user: User, db: db_dependency): # type: ignore
    user = db.query(models.User).filter(models.User.id == user_id).first()

    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    # Update fields
    user.username = updated_user.username
    db.commit()  
    return user


#posts api







