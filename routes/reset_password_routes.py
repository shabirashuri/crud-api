from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from datetime import datetime, timedelta
from jose import jwt
from database import Sessionlocal
from typing import Annotated
from models import User
from schema import Forgotpassword, Resetpassword
from utils.password_utils import hash_password
from utils.jwt_utils import SECRET_KEY, ALGORITHM
from utils.email_utils import send_email  


router = APIRouter()


def get_db():
    db = Sessionlocal()
    try:
        yield db
    finally:
        db.close()

db_dependency = Annotated[Session, Depends(get_db)]


# Send reset token by email
@router.post("/forgot-password")
def forgot_password(request: Forgotpassword, db: db_dependency):
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

    # Create the email message
    message = f"""
    Hello {user.email},

    You requested to reset your password.

    Use this reset token (valid for 15 minutes):

    {reset_token}

    """
    # Send the email
    send_email(user.email, "Password Reset Request", message)

    return {"message": "Password reset email sent. Check your inbox."}



# reset the password using token
@router.post("/reset-password")
def reset_password(request: Resetpassword, db: db_dependency):

    try:
        payload = jwt.decode(request.token, SECRET_KEY, algorithms=[ALGORITHM])

        if payload.get("type") != "password_reset":
            raise HTTPException(status_code=400, detail="Invalid token type")

        email = payload.get("sub")
        if email is None:
            raise HTTPException(status_code=400, detail="Invalid token data")

    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=400, detail="Reset token expired")
    except jwt.JWTError:
        raise HTTPException(status_code=400, detail="Invalid token")

    # Find user from decoded email
    user = db.query(User).filter(User.email == email).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    # Update password
    user.password = hash_password(request.new_password)
    db.commit()

    return {"message": "Password reset successfully"}
