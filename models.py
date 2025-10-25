from sqlalchemy import Integer, String, Column, Boolean, ForeignKey, UniqueConstraint
from database import Base
from sqlalchemy.orm import relationship


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    firstname = Column(String(50))
    lastname = Column(String(50))
    email = Column(String(50), unique=True, index=True)
    password = Column(String(200))

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
    comments = relationship("Comment", back_populates="post")  # ✅ fixed
    likes = relationship("Like", back_populates="post")        # ✅ fixed

class Comment(Base):
    __tablename__ = "comments"

    id = Column(Integer, primary_key=True, index=True)
    content = Column(String(300))
    post_id = Column(Integer, ForeignKey("posts.id", ondelete="CASCADE"))
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"))

    # Relationships
    user = relationship("User", back_populates="comments")
    post = relationship("Post", back_populates="comments")  # ✅ fixed


class Like(Base):
    __tablename__ = "likes"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"))
    post_id = Column(Integer, ForeignKey("posts.id", ondelete="CASCADE"))

    # Relationships
    user = relationship("User", back_populates="likes")
    post = relationship("Post", back_populates="likes")  # ✅ fixed

    # Prevent duplicate likes by same user on same post
    __table_args__ = (UniqueConstraint("user_id", "post_id", name="_user_post_uc"),)
