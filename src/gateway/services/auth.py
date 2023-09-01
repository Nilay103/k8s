import os, requests
from typing import Union
from typing import Dict

from wtforms.validators import ValidationError
from response import ErrorResponse, SuccessResponse


def check_user_login(request) -> Union[ErrorResponse, SuccessResponse]:
    auth = request.authorization
    if not auth:
        return ErrorResponse(
            msg="missing credentials",
            status=401
        )

    basicAuth = (auth.username, auth.password)

    response = requests.post(
        # f"http://{os.environ.get('AUTH_SVC_ADDRESS')}/login", auth=basicAuth TODO
        "http://localhost:5000/login", auth=basicAuth
    )
    return SuccessResponse(
        data=response.json(),
        status=response.status_code,
        nested=True
    )


def validate_token(request) -> Dict:
    if "Authorization" not in request.headers:
        raise ValidationError(message="missing credentials")

    _token: str = request.headers["Authorization"]
    if not _token:
        raise ValidationError(message="missing credentials")

    response = requests.post(
        # f"http://{os.environ.get('AUTH_SVC_ADDRESS')}/validate", TODO
        url=f"http://localhost:5000/validate",
        headers={"Authorization": _token},
    )

    if response.status_code == 200:
        return response.json()
    else:
        raise ValidationError(message="Login service failed.")
