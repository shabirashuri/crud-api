from pydantic import BaseModel

class Post(BaseModel):
    title : str
    content : str
    user_id : int

class User(BaseModel):
    firstname : str
    lastname : str
    email : str
    password : str