from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from datetime import datetime, timedelta
from jose import jwt
from database import Sessionlocal
from typing import Annotated
from models import User
from schema import Forgotpassword ,Resetpassword
from utils.password_utils import hash_password
from utils.jwt_utils import SECRET_KEY, ALGORITHM  # use same constants as login/register


router = APIRouter()


def get_db():
    db = Sessionlocal()
    try:   
        yield db
    finally:
        db.close()

db_dependency = Annotated[Session, Depends(get_db)]

 
@router.post("/forgot-password")
def forgot_password(request : Forgotpassword , db: db_dependency):
    user = db.query(User).filter(User.email == request.email).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    # Generate short-lived reset token (15 minutes)
    expire = datetime.utcnow() + timedelta(minutes=15)
    reset_token = jwt.encode(
        {"sub": user.email, "exp": expire, "type": "password_reset"},
        SECRET_KEY,
        algorithm=ALGORITHM
    )

    # For now, return the token (in real app you’d email it)
    return {"reset_token": reset_token, 
            "message": "Use this token to reset your password"}



@router.post("/reset-password")
def reset_password(request: Resetpassword, db: Session = Depends(get_db)):

    try:
       
        payload = jwt.decode(request.token, SECRET_KEY, algorithms=[ALGORITHM])

        if payload.get("type") != "password_reset":
            raise HTTPException(status_code=400, detail="Invalid token type")

        email = payload.get("sub")
        if email is None:
            raise HTTPException(status_code=400, detail="Invalid token data")

    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=400, detail="Reset token expired")
    except jwt.InvalidTokenError:
        raise HTTPException(status_code=400, detail="Invalid token")

    
    user = db.query(User).filter(User.email == email).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    
    user.password = hash_password(request.new_password)

    db.commit()

    return {"message": "Password reset successfully"}