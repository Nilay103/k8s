import os, gridfs

from celery import Celery
from flask import Flask, request, send_file
from flask_pymongo import PyMongo
from bson.objectid import ObjectId
from wtforms import ValidationError

from decorators import handle_api_exception
from response import SuccessResponse, ErrorResponse
from services.auth import check_user_login, validate_token
from services.upload import upload_file

server = Flask(__name__)

mongo_video = PyMongo(server, uri="mongodb://localhost:27017/videos")
mongo_mp3 = PyMongo(server, uri="mongodb://localhost:27017/mp3s")

fs_videos = gridfs.GridFS(mongo_video.db)
fs_mp3s = gridfs.GridFS(mongo_mp3.db)

server.config['CELERY_BROKER_URL'] = 'redis://localhost:6379/0'
server.config['CELERY_RESULT_BACKEND'] = 'redis://localhost:6379/0'

celery = Celery(server.name, broker=server.config['CELERY_BROKER_URL'])
celery.conf.update(server.config)


@server.route("/login", methods=["POST"])
@handle_api_exception
def login():
    return check_user_login(request)


@server.route("/upload", methods=["POST"])
@handle_api_exception
def upload():
    access_data = validate_token(request)

    if access_data["data"]["attributes"]["admin"]:
        if len(request.files) > 1 or len(request.files) < 1:
            raise ValidationError(message="Exactly 1 file required")

        for _, f in request.files.items():
            upload_file(file=f, collection=fs_videos, user=access_data["data"]["attributes"])

        return SuccessResponse(msg="Video uploaded successfully", status=200)
    else:
        return ErrorResponse(msg="Unauthorized", status=401)


@server.route("/download", methods=["GET"])
@handle_api_exception
def download():
    validate_token(request)

    fid_string = request.args.get("fid")
    if not fid_string:
        raise ValidationError(message="File id is required.")

    out = fs_mp3s.get(ObjectId(fid_string))
    return send_file(out, download_name=f"{fid_string}.mp3")


if __name__ == "__main__":
    server.run(host="0.0.0.0", port=8080, debug=True)
