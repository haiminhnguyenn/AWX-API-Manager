from app.extensions import db
from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column

class UserAccount(db.Model):
    username: Mapped[str] = mapped_column(String(100), primary_key=True)
    password: Mapped[str] = mapped_column(String(100), nullable=True)