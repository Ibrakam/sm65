from fastapi import FastAPI, Request, Form, status
from database import Base, engine
from api.user.main import user_router
from api.photo.main import photo_router
from api.post.main import post_router
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse, RedirectResponse
from database.userservice import get_all_or_exact_user, create_user_db
from database.postservice import all_user_posts, post_with_id
from api.user.schemas import UserSchema

templates = Jinja2Templates("templates")

app = FastAPI(docs_url="/docs")

Base.metadata.create_all(engine)

app.include_router(user_router)
app.include_router(photo_router)
app.include_router(post_router)



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
        response = RedirectResponse("/1", status_code=status.HTTP_303_SEE_OTHER)
        return response
    return {"status":0, "error": "Error"}

