import re

from pydantic import BaseModel, field_validator

from app.config.settings import settings


class SignUp(BaseModel):
    username: str
    password: str

    @field_validator("password")
    def validate_password(cls, value):
        if not re.match(settings.PASSWORD_REGEX, value):
            raise ValueError(
                "Password must contain at least one uppercase, one lowercase, one digit and one special character"
            )
        return value


class Login(BaseModel):
    username: str
    password: str
