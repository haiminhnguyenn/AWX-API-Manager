from celery import Celery
from app import app

def make_celery(app):
    celery = Celery(
        app.import_name,
        broker=app.config["CELERY_BROKER_URL"],
        backend=app.config["CELERY_RESULT_BACKEND"]
    )
    celery.conf.update(app.config)
    return celery

celery = make_celery(app)