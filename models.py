from sqlalchemy import Integer,String,Column,Boolean # type: ignore
from database import Base
from typing import List
from sqlalchemy.orm import relationship
from sqlalchemy import ForeignKey
from sqlalchemy import Integer
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column

class User(Base):
    __tablename__ = "user"

    id = Column(Integer,primary_key =  True, index = True )
    firstname  = Column(String(50))
    lastname = Column(String(50))
    email = Column(String(50))
    password = Column(String(200))
    posts = relationship("Post", back_populates="user")


class Post(Base):
    __tablename__ = "posts"

    id = Column(Integer,primary_key = True, index = True )
    title = Column(String(50))
    content = Column(String(100))
    user_id = Column(Integer , ForeignKey("user.id"))
    user = relationship("User", back_populates="posts")
    
