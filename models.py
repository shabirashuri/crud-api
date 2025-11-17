from sqlalchemy import Integer, String, Column, Boolean, ForeignKey, UniqueConstraint
from database import Base
from sqlalchemy.orm import relationship
from datetime import datetime, timedelta 
from sqlalchemy import DateTime


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    firstname = Column(String(50))
    lastname = Column(String(50))
    email = Column(String(50), unique=True, index=True)
    password = Column(String(200))
    role = Column(String(50), default="user") # for role based access

    # Relationships
    posts = relationship("Post", back_populates="user")
    comments = relationship("Comment", back_populates="user")
    likes = relationship("Like", back_populates="user")


class Post(Base):
    __tablename__ = "posts"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(50))
    content = Column(String(100))
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"))

    # Relationships
    user = relationship("User", back_populates="posts")
    comments = relationship("Comment", back_populates="post")  
    likes = relationship("Like", back_populates="post")        

class Comment(Base):
    __tablename__ = "comments"

    id = Column(Integer, primary_key=True, index=True)
    content = Column(String(300))
    post_id = Column(Integer, ForeignKey("posts.id", ondelete="CASCADE"))
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"))

    # Relationships
    user = relationship("User", back_populates="comments")
    post = relationship("Post", back_populates="comments") 


class Like(Base):
    __tablename__ = "likes"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"))
    post_id = Column(Integer, ForeignKey("posts.id", ondelete="CASCADE"))

    # Relationships
    user = relationship("User", back_populates="likes")
    post = relationship("Post", back_populates="likes")  

    # Prevent duplicate likes by same user on same post
    __table_args__ = (UniqueConstraint("user_id", "post_id", name="_user_post_uc"),)


# class PasswordReset(Base):
#     __tablename__ = "password_resets"

#     id = Column(Integer, primary_key=True, index=True)
#     email = Column(String(100), index=True, nullable=False)
#     otp_hash = Column(String(400), nullable=False)
#     expires_at = Column(DateTime, nullable=False)
#     verified = Column(Boolean, default=False)



class PasswordResetToken(Base):
    __tablename__ = "password_reset_tokens"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    token_hash = Column(String(100), nullable=False)
    expires_at = Column(DateTime, nullable=False)
    used = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    user = relationship("User")

