from fastapi import FastAPI, Request, Form, status, HTTPException, Depends
from database import Base, engine
from api.user.main import user_router
from api.photo.main import photo_router
from api.post.main import post_router
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse, RedirectResponse
from database.userservice import get_all_or_exact_user, create_user_db
from database.postservice import all_user_posts, post_with_id
from api.user.schemas import UserSchema
from pydantic import BaseModel
from typing import Optional
from fastapi.security import OAuth2PasswordRequestForm, OAuth2PasswordBearer
from config import algorithm, access_token_exp_minutes, secret_key
from datetime import timedelta, datetime
from jose import jwt

templates = Jinja2Templates("templates")

app = FastAPI(docs_url="/docs")

Base.metadata.create_all(engine)

app.include_router(user_router)
app.include_router(photo_router)
app.include_router(post_router)

"""
JWT SETTINGS
"""


class Token(BaseModel):
    access_token: str
    token_type: str


class User(BaseModel):
    username: str
    password: str


fake_db = {
    "johndoe":
        {
            "username": "johndoe",
            "password": "123"
        }
}


def verify_password(password1, password2):
    """

    :param password1: Пароль который вводит пользователь на сайте
    :param password2: Пароль который хранится в бд
    :return: True или False
    """
    return password1 == password2


def get_user(db, username):
    """

    :param db: Запрос к бд
    :param username: Ключ для получение пользователя
    :return: User(...)
    """

    if username in db:
        user_dict = db[username]
        return User(**user_dict)


def create_access_token(data, expire_date: Optional[timedelta] = 15):
    """
    Функция для создание jwt токена
    :param data: Данные которые будем шифровать
    :param expire_date: Какое колво времени будет работать токен
    :return: вернуть токен
    """

    to_encode = data.copy()

    expire = datetime.utcnow() + timedelta(minutes=int(access_token_exp_minutes))

    to_encode.update({"exp": expire})

    encoded_jwt = jwt.encode(to_encode, secret_key, algorithm=algorithm)

    return encoded_jwt


def authenticate_user(db, username, password):
    user = get_user(db, username)
    if user and verify_password(password, user.password):
        return user
    return False


@app.post("/token", response_model=Token)
async def login(form: OAuth2PasswordRequestForm = Depends()):
    user = authenticate_user(fake_db, form.username, form.password)
    if not user:
        return HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                             detail="Неправильный пароль или username")
    access_token = create_access_token(data={"sub": user.username})
    return {"access_token": access_token,
            "token_type": "bearer"}


oauth_schema = OAuth2PasswordBearer(tokenUrl="token")


async def get_current_user(token: str = Depends(oauth_schema)):
    exception = HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Error")
    try:
        payload = jwt.decode(token, secret_key, algorithms=[algorithm])

        username = payload.get("sub")
        if username is None:
            return exception
    except jwt.JWTError:
        return exception


@app.get("/register", response_class=HTMLResponse)
async def register_user_api(request: Request):
    return templates.TemplateResponse(request, name="register.html")


@app.get("/{uid}", include_in_schema=False, response_class=HTMLResponse)
async def main(request: Request, uid: int):
    exact_user = get_all_or_exact_user(user_id=uid)
    all_posts = all_user_posts(uid)
    return templates.TemplateResponse(request, name="index.html", context={
        "user": exact_user,
        "posts": all_posts
    })


# @app.get("/exact-post/{pid}", include_in_schema=False, response_class=HTMLResponse)
# async def main(request: Request, pid: int):
#     all_posts = post_with_id(pid)
#     return templates.TemplateResponse(request, name="index.html", context={
#         "posts": all_posts
#     })

# uvicorn main:app --reload


@app.post("/register", response_class=HTMLResponse)
async def register_user_api_post(request: Request,
                                 name: str = Form(...),
                                 surname: str = Form(...),
                                 username: str = Form(...),
                                 email: str = Form(...),
                                 password: str = Form(...),
                                 phone_number: str = Form(...),
                                 birthday: str = Form(...),
                                 city: str = Form(...)
                                 ):
    user = UserSchema(name=name, surname=surname, username=username,
                      email=email, phone_number=phone_number, password=password,
                      birthday=birthday, city=city)
    result = create_user_db(user)
    if result:
        response = RedirectResponse(f"/{result}", status_code=status.HTTP_303_SEE_OTHER)
        return response
    return {"status": 0, "error": "Error"}
