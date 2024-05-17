from fastapi.responses import ORJSONResponse


def client_side_error(user_msg: str, status_code: int = 400):
    return ORJSONResponse(
        content={"user_msg": user_msg, "dev_msg": user_msg}, status_code=status_code
    )


def internal_server_error(user_msg: str, error, status_code: int = 500):
    return ORJSONResponse(
        status_code=status_code,
        content={
            "userMsg": user_msg,
            "devMsg": str(error),
        },
    )


def send_data_with_info(data: dict, info: str, status_code: int = 200):
    return ORJSONResponse(content={"data": data, "info": info}, status_code=status_code)


def send_info(info: str, status_code: int = 200):
    return ORJSONResponse(content={"info": info}, status_code=status_code)
