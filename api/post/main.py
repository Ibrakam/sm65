from fastapi import APIRouter
from api.post.schemas import PostSchema, PostRead
from database.postservice import create_post, all_user_posts, post_with_id, change_post, delete_post

post_router = APIRouter(prefix="/post", tags=["PostAPI"])


# Создание поста
@post_router.post("/create_post", response_model=PostRead)
async def create_post_api(post: PostSchema):
    result = create_post(post)
    return {"status": 1, "message": result}


# Получение всех постов
@post_router.get("/get_posts", response_model=list[PostRead])
async def get_posts_api():
    result = all_user_posts()
    return {"status": 1, "message": result}


# Получение поста по ID
@post_router.get("/get_post/{post_id}", response_model=PostRead)
async def get_post_by_id_api(post_id: int):
    result = post_with_id(post_id)
    return {"status": 1, "message": result}


# Изменение поста
@post_router.put("/update_post/{post_id}", response_model=PostRead)
async def update_post_api(post_id: int, post: PostSchema):
    result = change_post(post_id, post)
    return {"status": 1, "message": result}


# Удаление поста
@post_router.delete("/delete_post/{post_id}")
async def delete_post_api(post_id: int):
    result = delete_post(post_id)
    return {"status": 1, "message": result}



