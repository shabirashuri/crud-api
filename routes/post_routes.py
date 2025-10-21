from fastapi import APIRouter, HTTPException, Depends, status
from typing import Annotated
from sqlalchemy.orm import Session
import models

from database import Sessionlocal
from schema import Post , Update_post


router = APIRouter()

# Dependency
def get_db():
    db = Sessionlocal()
    try:
        yield db
    finally:
        db.close()

db_dependency = Annotated[Session, Depends(get_db)]


@router.post("/", status_code=status.HTTP_201_CREATED)
async def create_user(post : Post, db: db_dependency):
    post = models.Post(**post.dict())
    db.add(post)
    db.commit()
    db.refresh(post)
    return {
        "msg" : "post added succefully",
        "post" : {
            "title" : post.title,
            "content" : post.content
        }
    }    

@router.get("/{user_id}/posts")
def get_posts_by_user(user_id: int, db: db_dependency):
 
    user = db.query(models.User).filter(models.User.id == user_id).first()

    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    return {"user": user.firstname, "posts": user.posts}

@router.put("/{user_id}/{post_id}",status_code=status.HTTP_200_OK)
def update_post( post_id:int,  updated_post: Update_post  , db :db_dependency):

    post = db.query(models.Post).filter(models.Post.id == post_id).first()

    if not post :
        raise HTTPException(status_code=404, detail="post not found")

    if updated_post.title is not None:
        post.title = updated_post.title
    if updated_post.content is not None:
        post.content = updated_post.content

    db.commit()
    db.refresh(post)
    return {"msg": "post updated successfully", "post": post}

@router.delete("{user_id}/{post_id}")
def delete_post(post_id :int ,db :db_dependency):
      post = db.query(models.Post).filter(models.Post.id == post_id).first()
      
      if not post :
        raise HTTPException(status_code=404, detail="post not found")
      
      db.delete(post)
      db.commit()

      return {"msg" : "post deleted succesfully", "post" : post}



    

    
