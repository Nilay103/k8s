import traceback
from functools import wraps

from response import ErrorResponse


def handle_api_exception(f):
    @wraps(f)
    def wrapper(*args, **kwargs):
        try:
            return f(*args, **kwargs)
        except:
            print(traceback.format_exc())
            return ErrorResponse(
                msg="Something went wrong.",
                status=500,
                data={
                    "traceback": traceback.format_exc()
                }
            )

    return wrapper
