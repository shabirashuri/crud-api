from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
import models
from database import Sessionlocal
from schema import LikeBase, LikeResponse
from utils.jwt_utils import decode_access_token
from typing import Annotated

router = APIRouter()

def get_db():
    db = Sessionlocal()
    try:   
        yield db
    finally:
        db.close()

db_dependency = Annotated[Session, Depends(get_db)]

@router.post("/", status_code=status.HTTP_201_CREATED)
def like_post(
    like_data: LikeBase,
    db: db_dependency,
    current_user: dict = Depends(decode_access_token)
):
    user_id = current_user["id"]
    post_id = like_data.post_id

    post = db.query(models.Post).filter(models.Post.id == post_id).first()
    if not post:
        raise HTTPException(status_code=404, detail="Post not found")

    # Check if already liked
    existing_like = db.query(models.Like).filter_by(user_id=user_id, post_id=post_id).first()
    if existing_like:                               
        raise HTTPException(status_code=400, detail="You already liked this post")

    new_like = models.Like(user_id=user_id, post_id=post_id)
    db.add(new_like)
    db.commit()
    db.refresh(new_like)
    return {"msg": "Post liked successfully", "like": new_like}


@router.delete("/{post_id}", status_code=status.HTTP_200_OK)
def unlike_post(
    post_id: int,
    db: db_dependency,
    current_user: dict = Depends(decode_access_token)
):
    user_id = current_user["id"]
    like = db.query(models.Like).filter_by(user_id=user_id, post_id=post_id).first()

    if not like:
        raise HTTPException(status_code=404, detail="Like not found")

    db.delete(like)
    db.commit()
    return {"msg": "Post unliked successfully"}


@router.get("/{post_id}", response_model=int)
def get_likes_count(post_id: int, db: db_dependency):
    count = db.query(models.Like).filter(models.Like.post_id == post_id).count()
    return count
