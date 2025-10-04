from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import jwt
from database.userservice import get_user_by_username

from config import secret_key, algorithm

oauth_schema = OAuth2PasswordBearer(tokenUrl="token")


async def get_current_user(token: str = Depends(oauth_schema)):
    exception = HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Error")
    try:
        payload = jwt.decode(token, secret_key, algorithms=[algorithm])
        print(payload)
        username = payload.get("sub")
        if username is None:
            return exception
    except jwt.JWTError:
        return exception
    user = get_user_by_username(username)
    print(user)
    if user:
        return user
    return exception



# async def get_current_use