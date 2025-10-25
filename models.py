from sqlalchemy import Integer,String,Column,Boolean # type: ignore
from database import Base
from typing import List
from sqlalchemy.orm import relationship
from sqlalchemy import ForeignKey
from sqlalchemy import Integer


class User(Base):
    __tablename__ = "user"

    id = Column(Integer,primary_key =  True, index = True )
    firstname  = Column(String(50))
    lastname = Column(String(50))
    email = Column(String(50))
    password = Column(String(200))
    posts = relationship("Post", back_populates="user")
    comments = relationship("Comment", back_populates="user")



class Post(Base):
    __tablename__ = "posts"
 
    id = Column(Integer,primary_key = True, index = True )
    title = Column(String(50))
    content = Column(String(100))
    user_id = Column(Integer , ForeignKey("user.id"))
    user = relationship("User", back_populates="posts")
    comments = relationship("Comment", back_populates="posts")

    

class Comment(Base):
    __tablename__ = "comments"

    id = Column(Integer, primary_key=True, index=True)
    content = Column(String(300))
    post_id = Column(Integer, ForeignKey("posts.id"))
    user_id = Column(Integer, ForeignKey("user.id"))

    user = relationship("User", back_populates="comments")
    post = relationship("Post", back_populates="comments")

