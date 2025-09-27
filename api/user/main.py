from fastapi import APIRouter
from api.user.schemas import UserSchema, UserRead
from database.userservice import create_user_db, get_all_or_exact_user

user_router = APIRouter(prefix="/user", tags=["UserApi"])


@user_router.post("/create_user", response_model=UserRead)
async def create_user_api(user: UserSchema):
    result = create_user_db(user)
    return {"status": 1, "message": result}


@user_router.get("/get_users")
async def get_user(user_id: int = 0):
    """

    :param user_id: Должны указать айди пользователя
    :return: должен возвращать в виде {status: int, message: bool}
    """
    result = get_all_or_exact_user(user_id=user_id)
    if result:
        return {"status": 1, "message": result}
    return {"status": 0, "message": result}
