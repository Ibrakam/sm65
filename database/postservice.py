from database import get_db
from database.models import UserPost


# Cоздание поста
def create_post(title, main_text, uid):
    with next(get_db()) as db:
        new_post = UserPost(title=title, main_text=main_text, uid=uid)
        db.add(new_post)
        db.commit()
        return True


# Получение всех постов пользователя - user_id
def all_user_posts(uid):
    with next(get_db()) as db:
        user_posts = db.query(UserPost).filter_by(uid=uid).all()
        return user_posts


# Получение определенного поста - post_id
def post_with_id(post_id):
    with next(get_db()) as db:
        post = db.query(UserPost).filter_by(id=post_id).first()
        return post


# Изменение поста
def change_post(post_id, change_info, new_info):
    with next(get_db()) as db:
        post = db.query(UserPost).filter_by(id=post_id).first()
        if post:
            if change_info == "title":
                post.title = new_info
            elif change_info == "main_text":
                post.main_text = new_info
            elif change_info == "uid":
                post.uid = new_info
            db.commit()
            return True
        return False


# Удаление поста
def delete_post(post_id):
    with next(get_db()) as db:
        db.query(UserPost).filter_by(id=post_id).delete()
        db.commit()
        return True
