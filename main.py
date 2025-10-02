from fastapi import FastAPI, Request
from database import Base, engine
from api.user.main import user_router
from api.photo.main import photo_router
from api.post.main import post_router
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
from database.userservice import get_all_or_exact_user
from database.postservice import all_user_posts, post_with_id

templates = Jinja2Templates("templates")

app = FastAPI(docs_url="/docs")

Base.metadata.create_all(engine)

app.include_router(user_router)
app.include_router(photo_router)
app.include_router(post_router)


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
