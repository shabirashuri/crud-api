from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from database import Sessionlocal
from typing import Annotated
import models, schema
from utils.jwt_utils import decode_access_token

router = APIRouter()


def get_db():
    db = Sessionlocal()
    try:   
        yield db
    finally:
        db.close()

db_dependency = Annotated[Session, Depends(get_db)]

# Create a Comment

@router.post("/{post_id}", status_code=status.HTTP_201_CREATED)
def create_comment(
    post_id: int,
    comment: schema.CommentCreate,
    db: db_dependency,
    current_user: dict = Depends(decode_access_token)
):
    post = db.query(models.Post).filter(models.Post.id == post_id).first()
    if not post:
        raise HTTPException(status_code=404, detail="Post not found")

    new_comment = models.Comment(
        content=comment.content,
        post_id=post.id,
        user_id=current_user["id"]
    )
    db.add(new_comment)
    db.commit()
    db.refresh(new_comment)
    return {"message": "Comment added successfully", "comment": new_comment}


# Get all comments for a post

@router.get("/{post_id}", response_model=list[schema.CommentResponse])
def get_comments_for_post(post_id: int, db: db_dependency):
    comments = db.query(models.Comment).filter(models.Comment.post_id == post_id).all()
    return comments
