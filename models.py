from sqlalchemy import Integer,String,Column,Boolean # type: ignore
from database import Base

class User(Base):
    __tablename__ = "user"

    id = Column(Integer,primary_key =  True, index = True )
    firstname  = Column(String(50))
    lastname = Column(String(50))
    email = Column(String(50))
    password = Column(String(200))


class Post():
    __tablename__ = "posts"

    id = Column(Integer,primary_key = True, index = True )
    title = Column(String(50))
    content = Column(String(100))
    use_id = Column(Integer)

    
