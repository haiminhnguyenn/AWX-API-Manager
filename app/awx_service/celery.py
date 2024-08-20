from celery import Celery

celery = Celery(
    __name__,
    broker="amqp://guest:guest@localhost:5672//"
)

celery.conf.update(
    result_backend='rpc://',
    imports=['app.awx_service.tasks'],  # Import mô-đun chứa tác vụ
)