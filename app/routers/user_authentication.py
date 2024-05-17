from fastapi import APIRouter, Depends

from app.core.exceptions import InvalidOperationError
from app.helpers import messages
from app.helpers.transformers import transform_user
from app.routers.responses import (
    client_side_error,
    internal_server_error,
    send_data_with_info,
)
from app.schemas.user_auth_schema import Login, SignUp
from app.services.user_service import UserService

router = APIRouter(
    prefix="/user",
    tags=["user authentication"],
)


@router.post("/signup")
def user_sign_up(payload: SignUp, user_service: UserService = Depends()):
    try:
        data = user_service.create_user(payload=payload)
        return send_data_with_info(
            info=messages.CREATE_SUCCESS + "user",
            data=data,
        )
    except InvalidOperationError as e:
        return client_side_error(
            user_msg=str(e),
        )
    except Exception as e:
        return internal_server_error(
            user_msg=messages.CREATE_FAILED + "user",
            error=str(e),
        )


@router.post("/login")
def user_login(payload: Login, user_service: UserService = Depends()):
    try:
        data = user_service.login_user(payload=payload)
        return send_data_with_info(
            info=messages.LOGIN_SUCCESS,
            data=data,
        )
    except InvalidOperationError as e:
        return client_side_error(
            user_msg=str(e),
        )
    except Exception as e:
        return internal_server_error(
            user_msg=messages.LOGIN_FAILED,
            error=str(e),
        )
