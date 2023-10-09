from celery import Celery
import os
from dotenv import load_dotenv

load_dotenv()

celery_app = Celery(
    'celery_config',
    broker=os.getenv('RABBIT_MQ_URL'),
    include=['plasticome.services.dbcan_service', 'plasticome.services.ecpred_service', 'plasticome.services.email_service' ]
    )

celery_app.autodiscover_tasks()