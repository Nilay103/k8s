import json
from typing import Dict

from flask import Response


class SuccessResponse(Response):
    def __init__(
            self,
            response_type: str = "",
            msg: str = "",
            status: int = 200,
            data: Dict = {},
            nested: bool = False
    ):
        payload = {
            "message": msg,
            "data": data,
            "response_type": response_type,
        } if not nested else data
        super().__init__(
            response=json.dumps(payload),
            status=status
        )


class ErrorResponse(Response):
    def __init__(
            self,
            response_type: str = "",
            msg: str = "",
            status: int = 500,
            data: Dict = {},
            nested: bool = False
    ):
        payload = {
            "message": msg,
            "data": data,
            "response_type": response_type,
        } if not nested else data
        super().__init__(
            response=json.dumps(payload),
            status=status
        )
