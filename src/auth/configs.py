import os

MYSQL_HOST = os.environ.get("MYSQL_HOST", "db")
MYSQL_USER = os.environ.get("MYSQL_USER", "root")
MYSQL_PASSWORD = os.environ.get("MYSQL_PASSWORD", "root")
MYSQL_DB = os.environ.get("MYSQL_DB", "auth")
MYSQL_PORT = os.environ.get("MYSQL_PORT", 3306)

JWT_SECRET = os.environ.get("JWT_SECRET", "default")