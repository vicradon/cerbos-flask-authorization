from sqlalchemy import Column, String, ForeignKey
from sqlalchemy.orm import relationship, Mapped, mapped_column
from werkzeug.security import generate_password_hash, check_password_hash
from app.utils.helpers import slugify
from app.extensions import db

class User(db.Model):
    __tablename__ = "users"
    id: Mapped[int] = mapped_column(primary_key=True)
    username: Mapped[str] = mapped_column(unique=True)
    email: Mapped[str] = mapped_column(unique=True)
    is_admin: Mapped[bool] = mapped_column(default=False)
    email_is_verified: Mapped[bool] = mapped_column(default=False)
    password_hash: Mapped[str] = mapped_column()

    posts: Mapped[list["Post"]] = relationship("Post", back_populates="user", cascade="all, delete-orphan")
    comments: Mapped[list["Comment"]] = relationship("Comment", back_populates="user", cascade="all, delete-orphan")

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)


class Post(db.Model):
    __tablename__ = "posts"
    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str] = mapped_column(unique=True)
    body: Mapped[str] = mapped_column()
    slug: Mapped[str] = mapped_column(unique=True)
    is_published: Mapped[bool] = mapped_column(default=False)

    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))

    user: Mapped["User"] = relationship("User", back_populates="posts")
    comments: Mapped[list["Comment"]] = relationship("Comment", back_populates="post", cascade="all, delete-orphan")

    def __init__(self, title, body, is_published=False):
        self.title = title
        self.body = body
        self.slug = slugify(title)
        self.is_published = is_published


class Comment(db.Model):
    __tablename__ = "comments"
    
    id: Mapped[int] = mapped_column(primary_key=True)
    body: Mapped[str] = mapped_column()

    post_id: Mapped[int] = mapped_column(ForeignKey("posts.id"))
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))

    post: Mapped["Post"] = relationship("Post", back_populates="comments")
    user: Mapped["User"] = relationship("User", back_populates="comments")
