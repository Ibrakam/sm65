from database import Base
from sqlalchemy import (String, Column, Integer, DateTime, ForeignKey)
from sqlalchemy.orm import relationship
from datetime import datetime


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, autoincrement=True, primary_key=True)
    name = Column(String(64), nullable=False)
    surname = Column(String(64), nullable=False)
    username = Column(String(64), nullable=False, unique=True)
    email = Column(String(64), nullable=False, unique=True)
    password = Column(String(64), nullable=False)
    phone_number = Column(String, nullable=False, unique=True)
    birthday = Column(String(64), nullable=False)
    city = Column(String, default="Tashkent")
    reg_date = Column(DateTime, default=datetime.now())

    post_fk = relationship("UserPost", back_populates="user_fk", cascade="all, delete-orphan")
    comment_fk = relationship("Comment", back_populates="user_fk", cascade="all, delete-orphan")


class UserPost(Base):
    __tablename__ = "posts"

    id = Column(Integer, autoincrement=True, primary_key=True)
    title = Column(String(150), nullable=False)
    main_text = Column(String(255), nullable=False)
    uid = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"))
    reg_date = Column(DateTime, default=datetime.now())

    user_fk = relationship("User", back_populates="post_fk", lazy="joined")
    photo_fk = relationship("PostPhoto", back_populates="post_fk", cascade="all, delete-orphan")
    comment_fk = relationship("Comment", back_populates="post_fk", cascade="all, delete-orphan")


class Comment(Base):
    __tablename__ = "comment"

    id = Column(Integer, autoincrement=True, primary_key=True)
    text = Column(String(150), nullable=False)
    uid = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"))
    pid = Column(Integer, ForeignKey("posts.id", ondelete="CASCADE"))
    reg_date = Column(DateTime, default=datetime.now())

    user_fk = relationship("User", back_populates="comment_fk", lazy="joined")
    post_fk = relationship("UserPost", back_populates="comment_fk", lazy="joined")


class PostPhoto(Base):
    __tablename__ = "photos"

    id = Column(Integer, autoincrement=True, primary_key=True)
    pid = Column(Integer, ForeignKey("posts.id", ondelete="CASCADE"))
    reg_date = Column(DateTime, default=datetime.now())
    photo_path = Column(String, nullable=False)

    post_fk = relationship("UserPost", back_populates="photo_fk", lazy="joined")


"""
def create_photo(pid, photo_path):
PostPhoto(pid=pid, photo_path=)
"""