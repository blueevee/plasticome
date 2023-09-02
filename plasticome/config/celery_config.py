from celery import Celery


celery_app = Celery(
    broker='pyamqp://URL DO HOST (USAR RABBITMQ)'
)