import jwt, datetime, os
from flask import request

from decorators import handle_api_exception
from response import SuccessResponse, ErrorResponse
from flask import Flask
from flask_mysqldb import MySQL

server = Flask(__name__)

# config
server.config["MYSQL_HOST"] = os.environ.get("MYSQL_HOST")
server.config["MYSQL_USER"] = os.environ.get("MYSQL_USER", "root")
server.config["MYSQL_PASSWORD"] = os.environ.get("MYSQL_PASSWORD")
server.config["MYSQL_DB"] = os.environ.get("MYSQL_DB", "auth")
server.config["MYSQL_PORT"] = os.environ.get("MYSQL_PORT")

mysql = MySQL()
mysql.init_app(server)


@server.route("/login", methods=["POST"])
@handle_api_exception
def login():
    """ Login view lives here. It will check user from auth db.

    :return:
    :rtype:
    """
    auth = request.authorization
    if not auth:
        return "missing credentials", 401

    # check db for username and password
    cur = mysql.connection.cursor()
    res = cur.execute(
        "SELECT email, password FROM user WHERE email=%s", (auth.username,)
    )

    if res > 0:
        user_row = cur.fetchone()
        email = user_row[0]
        password = user_row[1]

        if auth.username != email or auth.password != password:
            return ErrorResponse(
                msg="invalid credentials",
                status=400
            )
        else:
            return SuccessResponse(
                data={
                    "auth_token": createJWT(
                        username=auth.username,
                        secret=os.environ.get("JWT_SECRET", "default"),
                        is_admin=True
                    )
                },
                status=200
            )
    else:
        return ErrorResponse(
            msg="invalid credentials",
            status=400
        )


@server.route("/validate", methods=["POST"])
@handle_api_exception
def validate():
    """validate user view lives here. it will fetch token from headers and validates jwt token.

    :return:
    :rtype:
    """
    encoded_jwt = request.headers["Authorization"]

    if not encoded_jwt:
        return ErrorResponse(
            msg="missing credentials",
            status=401
        )

    encoded_jwt = encoded_jwt.split(" ")[1]
    decoded = jwt.decode(
        encoded_jwt, os.environ.get("JWT_SECRET"), algorithms=["HS256"]
    )
    return SuccessResponse(
        data={
            "attributes": decoded
        },
        status=200
    )


def createJWT(username: str, secret: str, is_admin: bool = False):
    """ function to create JWT

    :param username: username
    :type username: string
    :param secret: secret key to create JWT
    :type secret: string
    :param is_admin: admin check
    :type is_admin: bool
    :return: token value
    :rtype: encoded string
    """
    return jwt.encode(
        {
            "username": username,
            "exp": datetime.datetime.now(tz=datetime.timezone.utc)
            + datetime.timedelta(days=1),
            "iat": datetime.datetime.utcnow(),
            "admin": is_admin,
        },
        secret,
        algorithm="HS256",
    )


if __name__ == "__main__":
    server.run(host="0.0.0.0", port=5000)
