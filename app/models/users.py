from sqlalchemy import Column, String

from app.models.base_model import BaseModel


class User(BaseModel):
    __tablename__ = "users"

    username = Column(String(length=20), nullable=False)
    password = Column(String(length=100), nullable=False)

    def __str__(self):
        return self.username
