from celery import Celery
import os
from dotenv import load_dotenv

load_dotenv(override=True)

celery_app = Celery(
    'celery_config',
    broker=os.getenv('RABBIT_MQ_URL'),
    include=['plasticome.services.dbcan_service', 'plasticome.services.ecpred_service', 'plasticome.services.email_service', 'plasticome.services.cazy_filter_service', 'plasticome.services.analysis_result_service' ]
    )
