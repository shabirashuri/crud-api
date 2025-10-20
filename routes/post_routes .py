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


