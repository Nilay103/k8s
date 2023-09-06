import os

AUTH_SVC_ADDRESS = os.environ.get("AUTH_SVC_ADDRESS")
NOTIFICATION_SVC_ADDRESS = os.environ.get("NOTIFICATION_SVC_ADDRESS")

MONGO_HOST = os.environ.get("MONGO_HOST")
MONGO_PORT = os.environ.get("MONGO_PORT", 27017)

REDIS_HOST = os.environ.get("REDIS_HOST")
