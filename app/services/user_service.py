from fastapi import Depends

from app.core.exceptions import InvalidOperationError, NotFoundError
from app.core.security import generate_access_token, verify_password
from app.helpers import messages
from app.helpers.transformers import transform_user
from app.repository.users_repository import UserRepository
from app.schemas.user_auth_schema import Login
from app.services.base_service import BaseService


class UserService(BaseService):
    def __init__(self, repository: UserRepository = Depends(UserRepository)):
        super().__init__(repository)

    def create_user(self, payload):
        existing_user = self.repository.get_user_by_username(payload.username)
        if existing_user:
            raise InvalidOperationError(messages.ALREADY_EXISTS + "username")
        user = self.repository.create_user(payload)
        return transform_user(user)

    def login_user(self, payload: Login):
        user = self.repository.get_user_by_username(payload.username)
        if not user:
            raise NotFoundError(messages.NOT_FOUND + "user")

        if not verify_password(payload.password, user.password):
            raise InvalidOperationError(messages.INVALID_CREDENTIALS)
        try:
            user = transform_user(user)

            access_token, expires = generate_access_token(user)

            return {"access_token": access_token, "expires": expires, "user": user}
        except Exception as e:
            raise e
