from fastapi import Depends, HTTPException, status, Request
from fastapi.security import OAuth2PasswordBearer
from jose import jwt, JWTError
from database.userservice import get_user_by_username
from config import secret_key, algorithm

# Allow dependency to NOT auto-raise so we can fall back to cookie when header is missing (browser case)
oauth_schema = OAuth2PasswordBearer(tokenUrl="/token", auto_error=False)


def _credentials_exception() -> HTTPException:
    return HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Not authenticated",
        headers={"WWW-Authenticate": "Bearer"},
    )


async def get_current_user(request: Request, token: str | None = Depends(oauth_schema)):
    """
    Tries to read access token from the Authorization header (Swagger use‑case).
    If absent, falls back to the `access_token` cookie (browser login form use‑case).
    Expects the cookie value to optionally include the "Bearer " prefix.
    """
    # 1) Fallback to cookie if header isn't present
    if not token:
        token = request.cookies.get("access_token")
        print(token)
        if token and token.startswith("Bearer "):
            token = token.split(" ", 1)[1]

    if not token:
        raise _credentials_exception()

    try:
        payload = jwt.decode(token, secret_key, algorithms=[algorithm])
        username: str | None = payload.get("sub")
        if username is None:
            raise _credentials_exception()
    except JWTError:
        raise _credentials_exception()

    user = get_user_by_username(username)
    if not user:
        raise _credentials_exception()

    return user



# async def get_current_use</file>