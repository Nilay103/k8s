import os

MYSQL_HOST = os.environ.get("MYSQL_HOST")
MYSQL_USER = os.environ.get("MYSQL_USER")
MYSQL_PASSWORD = os.environ.get("MYSQL_PASSWORD")
MYSQL_DB = os.environ.get("MYSQL_DB", "auth")
MYSQL_PORT = int(os.environ.get("MYSQL_PORT", 3306))

JWT_SECRET = os.environ.get("JWT_SECRET", "default")
