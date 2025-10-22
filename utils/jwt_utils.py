# jwt_utils.py

from datetime import datetime, timedelta
from jose import jwt, JWTError
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt

# Secret key for JWT
SECRET_KEY = "tyrtydf@#544564689y879b)()%$"  
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 40000

# -------------------------------
# Create a JWT access token
# -------------------------------

def create_access_token(data: dict, email: str):
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



# -------------------------------
# Verify and decode a JWT token
# -------------------------------
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


def decode_access_token(token: str = Depends(oauth2_scheme)):
    try:
        # Decode the token
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        id  = payload.get("id")
        user_email: str = payload.get("email")  # "sub" usually stores the user identifier
        if user_email is None:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token")
        return {"id":id,"email": user_email}

    except JWTError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid or expired token")
    
# decoded_token = decode_access_token(token)
# print(decoded_token)