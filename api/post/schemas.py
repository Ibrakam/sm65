from pydantic import BaseModel
from typing import Optional
from datetime import datetime


class PostSchema(BaseModel):
    title: str
    main_text: str
    uid: int


class PostRead(BaseModel):
    status: int
    message: bool
