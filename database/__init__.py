from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

# Указываем тип бд(sqlite3, postgres)
SQL_DATABASE = "sqlite:///sm65.db"

engine = create_engine(SQL_DATABASE)

# Создаем сессию что бы хранить данные
SessionLocal = sessionmaker(bind=engine)

# Создаем плноценную базу(django=models.Model)
Base = declarative_base()


# ПОдключение к бд
def get_db():
    db = SessionLocal()
    try:
        yield db
    except Exception:
        db.rollback()
        raise
    finally:
        db.close()

