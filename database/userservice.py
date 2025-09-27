from database import get_db
from database.models import User


# Функия для добавления пользователя в бд
def create_user_db(name, surname, username, password, email, phone_number, birthday, city):
    with next(get_db()) as db:
        new_user = User(name=name, surname=surname, username=username, password=password, email=email,
                        phone_number=phone_number, birthday=birthday, city=city)
        db.add(new_user)
        db.commit()
        return True

# Получение всех или определенного пользователя
def get_all_or_exact_user(user_id=0):
    with next(get_db()) as db:
        if user_id:
            exact_user = db.query(User).filter_by(id=user_id).first()
            if exact_user:
                return exact_user
            return False
        all_users = db.query(User).all()
        return all_users


# Удаление пользователя из бд
def delete_user_db(user_id):
    with next(get_db()) as db:
        db.query(User).filter_by(id=user_id).delete()
        db.commit()
        return True



# Изменение пользователя
def update_user_db(user_id, change_info, new_info):
    with next(get_db()) as db:
        to_update_user = db.query(User).filter_by(id=user_id).first()
        if to_update_user:
            if change_info == "name":
                to_update_user.name = new_info
            elif change_info == "email":
                to_update_user.email = new_info
            elif change_info == "password":
                to_update_user.password = new_info
            elif change_info == "surname":
                to_update_user.surname = new_info
            elif change_info == "city":
                to_update_user.city = new_info
            elif change_info == "birthday":
                to_update_user.birthday = new_info
            elif change_info == "phone_number":
                to_update_user.phone_number = new_info
            elif change_info == "username":
                to_update_user.username = new_info
            db.commit()
            return True
        return False
