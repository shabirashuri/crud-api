from pydantic import BaseModel
from typing import Optional

class Post(BaseModel):
    title : str
    content : str
    user_id : int

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