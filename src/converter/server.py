import os
import tempfile
import traceback

import gridfs
from bson import ObjectId
from flask import Flask, request, send_file
from celery import Celery, Task
from celery import shared_task
from flask_pymongo import PyMongo
from moviepy.editor import VideoFileClip
from wtforms import ValidationError

from configs import MONGO_HOST, REDIS_HOST, MONGO_PORT
from services.auth import check_user_login, validate_token
from services.decorators import handle_api_exception
from services.notifications import send_email_ns
from services.response import SuccessResponse

server = Flask(__name__)


def celery_init_app(app: Flask) -> Celery:
    class FlaskTask(Task):
        def __call__(self, *args: object, **kwargs: object) -> object:
            with app.app_context():
                return self.run(*args, **kwargs)

    celery_app = Celery(app.name, task_cls=FlaskTask)
    celery_app.config_from_object(app.config["CELERY"])
    celery_app.set_default()
    app.extensions["celery"] = celery_app
    return celery_app


server.config.from_mapping(
    CELERY=dict(
        broker_url=f"redis://{REDIS_HOST}",
        result_backend=f"redis://{REDIS_HOST}",
        task_ignore_result=True,
    ),
)

mongo_video = PyMongo(server, uri=f"mongodb://{MONGO_HOST}:{MONGO_PORT}/videos")
mongo_mp3 = PyMongo(server, uri=f"mongodb://{MONGO_HOST}:{MONGO_PORT}/mp3s")

db_videos = gridfs.GridFS(mongo_video.db)
db_mp3s = gridfs.GridFS(mongo_mp3.db)
celery_app = celery_init_app(server)


@shared_task(ignore_result=False)
def upload_file(**kwargs):
    try:
        file_data = kwargs["file_data"]
        file_name = kwargs["file_name"]

        # write data in temp file.
        vid_file_path = tempfile.gettempdir() + "/" + file_name
        with open(vid_file_path, "wb") as file_obj:
            file_obj.write(file_data)

        video_id = db_videos.put(file_data)

        # create audio from temp video file
        audio = VideoFileClip(vid_file_path).audio

        # write audio to the file
        audio_file_path = tempfile.gettempdir() + f"/{video_id}.mp3"
        audio.write_audiofile(audio_file_path)

        # save file to mongo
        f = open(audio_file_path, "rb")
        data = f.read()
        audio_id = db_mp3s.put(data)

        send_email_ns(payload_data={
            "mp3_fid": str(audio_id),
            "username": kwargs['user']['username']
        })
        f.close()
        os.remove(audio_file_path)
    except Exception:
        print(traceback.format_exc())


@server.route("/celery_check", methods=["GET"])
def celery_check():
    upload_file.delay()
    return "success"


@server.route("/login", methods=["POST"])
@handle_api_exception
def login():
    return check_user_login(request)


@server.route("/upload", methods=["POST"])
@handle_api_exception
def upload():
    access_data = validate_token(request)

    if len(request.files) > 1 or len(request.files) < 1:
        raise ValidationError(message="Exactly 1 file required")

    for _, f in request.files.items():
        upload_file.delay(**{
            "file_data": f.read(),
            "file_name": f.filename,
            "user": access_data["data"]["attributes"]
        })

    return SuccessResponse(msg="Video upload request accepted", status=200)


@server.route("/download", methods=["GET"])
@handle_api_exception
def download():
    validate_token(request)

    fid_string = request.args.get("fid")
    if not fid_string:
        raise ValidationError(message="File id is required.")

    out = db_mp3s.get(ObjectId(fid_string))
    return send_file(out, download_name=f"{fid_string}.mp3")


if __name__ == "__main__":
    server.run(host="0.0.0.0", port=8080, debug=True)
