from fastapi import FastAPI
from database import Base, engine
from api.user.main import user_router
from api.photo.main import photo_router

app = FastAPI(docs_url="/")

Base.metadata.create_all(engine)

app.include_router(user_router)
app.include_router(photo_router)
