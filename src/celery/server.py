from flask import Flask
from celery import Celery, Task
from celery import shared_task

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
        broker_url="redis://localhost",
        result_backend="redis://localhost",
        task_ignore_result=True,
    ),
)
celery_app = celery_init_app(server)


@shared_task(ignore_result=False)
def add_together():
    print("Hello world")


@server.route("/celery_check", methods=["GET"])
def celery_check():
    add_together.delay()
    return "success"


if __name__ == "__main__":
    server.run(host="0.0.0.0", port=5050)
