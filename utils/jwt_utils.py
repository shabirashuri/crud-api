from datetime import datetime, timedelta
from jose import jwt, JWTError
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from dotenv import load_dotenv
import os


load_dotenv()

# Secret key for JWT
SECRET_KEY = os.getenv("SECRET_KEY")
REFRESH_SECRET_KEY = os.getenv("REFRESH_SECRET_KEY")
ALGORITHM = os.getenv("ALGORITHM", "HS256")
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", 30))
REFRESH_TOKEN_EXPIRE_DAYS = int(os.getenv("REFRESH_TOKEN_EXPIRE_DAYS", 7))
 


# Create a JWT access token

def create_access_token(data: dict, email: str ):
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)

    to_encode.update({
        "email": email,
        "exp": expire
    })

    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


# Example test
# token = create_access_token({"id": 1,"name": "ali"}, "saqlain@gmail.com")
# print(token)

def create_refresh_token(data: dict,email: str):
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(days=REFRESH_TOKEN_EXPIRE_DAYS)
    to_encode.update({
        "email": email,
        "exp": expire
    })
    encoded_jwt = jwt.encode(to_encode, REFRESH_SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt



# Verify and decode a JWT token

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


def decode_access_token(token: str = Depends(oauth2_scheme)):
    try:
        # Decode the token
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        id  = payload.get("id")
        user_email: str = payload.get("email")
        user_role : str = payload.get("role") # "sub" usually stores the user identifier
        if user_email is None:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token")
        return {"id":id,"email": user_email,}

    except JWTError:
        return None
    

def decode_refresh_token(refresh_token: str):
    try:
        # Decode using refresh secret key
        payload = jwt.decode(refresh_token, REFRESH_SECRET_KEY, algorithms=[ALGORITHM])

        id = payload.get("id")
        user_email: str = payload.get("email")

        if user_email is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid refresh token"
            )

        # Return decoded data
        return {"id": id, "email": user_email}
    except JWTError:
        return None
    
# decoded_token = decode_access_token(token)
# print(decoded_token)