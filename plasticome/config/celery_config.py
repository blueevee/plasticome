from celery import Celery
import os
from dotenv import load_dotenv

load_dotenv()

celery_app = Celery(
    'celery_config',
    broker=os.getenv('RABBIT_MQ_URL'),
    backend=os.getenv('REDIS_URL'),
    include=['plasticome.services.dbcan_service', 'plasticome.services.ecpred_service']
    )

# TODO passos:
# Quando definir a função usar odecorator @app.task()
# Quando chamar a função que precisa do celery usar fuction.delay()
#  Rodar o rabbit MQ pro celery funcionar
# Ativar o celery em um terminal : celery -A celery_config worker --loglevel=INFO --pool=solo
# FLOWER é uma app de visualização das tarefas celery: celery -A `file` flower --adress=127.0.0.1 --port=5566
# Ver doc do celery e botar p rodar

# celery = Celery(
#     'myapp',
#     broker='redis://localhost:6379/0',  # URL do Redis
#     backend='redis://localhost:6379/0',  # URL do Redis como backend
#     include=['plasticome.services.ecpred_service.run_ecpred_container'],  # Especifique os módulos que contêm tarefas do Celery
# )

# # Configuração adicional do Celery (se necessário)
celery_app.autodiscover_tasks()
celery_app.conf.update(
    result_expires=3600,
)