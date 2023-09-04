import gridfs
from flask import Flask, request
from flask_pymongo import PyMongo

from services.decorators import handle_api_exception
from services.response import SuccessResponse
from services.send_email import send_email_ns

server = Flask(__name__)

mongo_mp3 = PyMongo(server, uri="mongodb://localhost:27017/mp3s")
db_mp3s = gridfs.GridFS(mongo_mp3.db)


@server.route("/send_ns", methods=["POST"])
@handle_api_exception
def send_ns():
    payload_data = request.get_json(request.data)
    send_email_ns(message=payload_data, db_mp3=db_mp3s)

    return SuccessResponse(
        msg="Email sent successfully"
    )


if __name__ == "__main__":
    server.run(host="0.0.0.0", port=5055, debug=True)
