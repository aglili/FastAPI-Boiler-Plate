from app.models.users import User


def transform_user(user: User):
    return {
        "id": user.id,
        "username": user.username,
        "created_at": user.created_at,
    }
