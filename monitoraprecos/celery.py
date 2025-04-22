import os
from celery import Celery
from celery.schedules import crontab


os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'monitoraprecos.settings')

app = Celery('monitoraprecos')
app.config_from_object('django.conf:settings', namespace='CELERY')

# Adicione explicitamente o app scraper para descoberta de tarefas
app.autodiscover_tasks(['core', 'scraper'])

app.conf.beat_schedule = {
    'verificar-produtos-a-cada-hora': {
        'task': 'scraper.tasks.verificar_todos_produtos',
        'schedule': crontab(minute=0),  # Executar a cada hora
        'args': (20, 200),  # 20 produtos por lote, máximo de 200 produtos por hora
    },
    'atualizar-posicoes-fila-diariamente': {
        'task': 'scraper.tasks.atualizar_posicoes_fila',
        'schedule': crontab(hour=0, minute=0),  # Executar uma vez por dia à meia-noite
    },
}

@app.task(bind=True)
def debug_task(self):
    print(f'Request: {self.request!r}')