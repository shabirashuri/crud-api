from pydantic import BaseModel
from typing import Optional

# login
class login(BaseModel):
    email : str
    password : str


class TokenRefreshRequest(BaseModel):
    refresh_token: str



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


# comments schema


class Comment(BaseModel):
    content: str

class CommentCreate(Comment):
    pass

class CommentResponse(Comment):
    id: int
    user_id: int
    post_id: int

    class Config:
        orm_mode = True


#   likes schema

class LikeBase(BaseModel):
    post_id: int

class LikeResponse(BaseModel):
    id: int
    user_id: int
    post_id: int


    class Config:
        orm_mode = True