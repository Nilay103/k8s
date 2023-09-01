import traceback
from functools import wraps

from wtforms.validators import ValidationError

from response import ErrorResponse


def handle_api_exception(f):
    @wraps(f)
    def wrapper(*args, **kwargs):
        try:
            return f(*args, **kwargs)
        except ValidationError as e:
            print(traceback.format_exc())
            return ErrorResponse(
                msg="API exception happened",
                status=403,
                data={
                    "traceback": traceback.format_exc()
                }
            )
        except Exception:
            print(traceback.format_exc())
            return ErrorResponse(
                msg="Something went wrong.",
                status=500,
                data={
                    "traceback": traceback.format_exc()
                }
            )

    return wrapper
