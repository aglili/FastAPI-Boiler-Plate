import structlog
from fastapi import Depends
from sqlalchemy.orm import Session

from app.config.database_config import get_db
from app.core.security import hash_password
from app.models.users import User
from app.repository.base_repository import BaseRepository
from app.schemas.user_auth_schema import SignUp


class UserRepository(BaseRepository):
    def __init__(self, db: Session = Depends(get_db)) -> None:
        super().__init__(User, db)

    def create_user(self, schema):
        details = SignUp(**schema.dict())
        details.password = hash_password(details.password)
        return self.create(details)

    def get_user_by_username(self, username):
        return self.db.query(self.model).filter(self.model.username == username).first()
