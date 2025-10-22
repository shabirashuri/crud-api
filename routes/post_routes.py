from fastapi import APIRouter, HTTPException, Depends, status
from typing import Annotated
from sqlalchemy.orm import Session
import models

from database import Sessionlocal
from schema import Post , Update_post

from utils.jwt_utils import decode_access_token

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
async def create_post(
    post: Post,
    db: db_dependency,
    current_user: dict = Depends(decode_access_token)
):
    print(f"USER DATA: {current_user}")

    # Create a new post manually
    new_post = models.Post()
    new_post.title = post.title
    new_post.content = post.content

    # Associate post with the logged-in user (foreign key)
    new_post.user_id = current_user["id"]

    # Save to DB
    db.add(new_post)
    db.commit()
    db.refresh(new_post)

    return {
        "msg": "Post added successfully",
        "post": {
            "title": new_post.title,
            "content": new_post.content
        }
    }




@router.get("/",status_code=status.HTTP_200_OK)
def get_posts_by_user(
                      db: db_dependency,
                      current_user: dict = Depends(decode_access_token)):
    
    user_id = current_user["id"]

    user = db.query(models.User).filter(models.User.id == user_id).first()
    
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
   
    return {
        "user": user.firstname,
        "posts": [{"title": post.title, "content": post.content} for post in user.posts]
    }



@router.put("/{post_id}",status_code=status.HTTP_200_OK)
def update_post( post_id:int, 
                 updated_post: Update_post  ,
                   db :db_dependency,
                   current_user: dict = Depends(decode_access_token)):

    user_id = current_user["id"]
    

    post = db.query(models.Post).filter(models.Post.id == post_id).first()

    if not post :
        raise HTTPException(status_code=404, detail="post not found")
    
    if post.user_id != user_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to update this post"
        )

    if updated_post.title is not None:
        post.title = updated_post.title
    if updated_post.content is not None:
        post.content = updated_post.content

    db.commit()
    db.refresh(post)
    return {"msg": "post updated successfully", "post": post}



@router.delete("/{post_id}")
def delete_post(post_id :int ,
                db :db_dependency,
                current_user: dict = Depends(decode_access_token)):
      
      user_id = current_user["id"]
      
      
      post = db.query(models.Post).filter(models.Post.id == post_id).first()
      
      if not post :
        raise HTTPException(status_code=404, detail="post not found")
      
      if post.user_id != user_id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Not authorized to update this post"
        )
      
      db.delete(post)
      db.commit()

      return {"msg" : "post deleted succesfully", "post" : post}



    

    
