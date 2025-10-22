from pydantic import BaseModel
from typing import Optional



# user schema
class User(BaseModel):
    firstname : Optional[str] = None
    lastname :Optional[str] = None
    email : str
    password : str


class User_update(BaseModel):
    firstname : Optional[str] = None
    lastname : Optional[str] = None
    email : Optional[str] = None
    password : Optional[str] = None


    # posts schema

class Post(BaseModel):
    title : Optional[str] = None
    content : str
    

class Update_post(BaseModel) :
    title : Optional[str] = None
    content : Optional[str] = None
