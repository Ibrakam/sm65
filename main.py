from fastapi import FastAPI, Request, Form, status, HTTPException, Depends
from database import Base, engine
from api.user.main import user_router
from api.photo.main import photo_router
from api.post.main import post_router
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse, RedirectResponse
from database.userservice import get_all_or_exact_user, create_user_db, get_user_by_username
from database.postservice import all_user_posts, post_with_id
from api.user.schemas import UserSchema
from pydantic import BaseModel
from typing import Optional
from fastapi.security import OAuth2PasswordRequestForm, OAuth2PasswordBearer
from config import algorithm, access_token_exp_minutes, secret_key
from datetime import timedelta, datetime
from jose import jwt
from deps import get_current_user


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


def authenticate_user(username, password):
    user = get_user_by_username(username)
    if user and verify_password(password, user.password):
        return user
    return False


@app.post("/token", response_model=Token)
async def login(form: OAuth2PasswordRequestForm = Depends()):
    user = authenticate_user(form.username, form.password)
    if not user:
        return HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                             detail="Неправильный пароль или username")
    access_token = create_access_token(data={"sub": user.username})
    return {"access_token": access_token,
            "token_type": "bearer"}


@app.get("/user/me", response_model=UserSchema)
async def get_current_user_api(user: UserSchema = Depends(get_current_user)):
    return user


@app.get("/login", response_class=HTMLResponse)
async def login_html(request: Request):
    return templates.TemplateResponse(request, name="login.html")


@app.post("/login", response_class=HTMLResponse)
async def login_form(username: str = Form(...),
                     password: str = Form(...)):
    user = get_user_by_username(username)
    if not user and not verify_password(password, user.password):
        return HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                             detail="Неправильный пароль или username")
    token = create_access_token(data={"sub": user.username})
    print(token)
    response = RedirectResponse(url="/", status_code=status.HTTP_303_SEE_OTHER)
    response.set_cookie(
        key="access_token",
        value=f"Bearer {token}",
        httponly=True,  # чтобы JS не видел
        samesite="lax",  # норм для обычных переходов
        # secure=True,   # включи на HTTPS
        max_age=60 * 60 * 24  # 1 день, подбери как нужно
    )
    return response


@app.get("/register", response_class=HTMLResponse)
async def register_user_api(request: Request):
    return templates.TemplateResponse(request, name="register.html")


@app.get("/", include_in_schema=False, response_class=HTMLResponse)
async def main(request: Request, current_user: UserSchema = Depends(get_current_user)):
    all_posts = all_user_posts(current_user.id)
    print(current_user)
    return templates.TemplateResponse(request, name="index.html", context={
        "user": current_user,
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
