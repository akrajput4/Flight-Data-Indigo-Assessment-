from kombu import Queue, Exchange
from utils.environment_configs import EnvironmentConfigs as env

broker_url = f'{env.broker_protocol}://{env.broker_username}:{env.broker_password}@{env.broker_host}:{env.broker_port}'
accept_content = ['application/json']
result_serializer = 'json'
task_serializer = 'json'
timezone = 'Asia/Kolkata'
result_backend_url = f'{env.result_backend_protocol}://{env.result_backend_username}:{env.result_backend_password}@{env.result_backend_host}:{env.result_backend_port}/{env.result_backend_db}'

# QUEUE SETTINGS
task_default_queue = f'{env.service_queue}'
task_default_exchange = f'{env.service_queue}'
task_default_exchange_type = 'direct'
task_default_routing_key = f'{env.service_queue}'
task_queues = (
    Queue(name=f'{env.service_queue}', exchange=Exchange(name=f'{env.service_queue}', type='direct'),
          routing_key=f'{env.service_queue}'),
)


# CELERY BEAT
beat_scheduler = 'django_celery_beat.schedulers:DatabaseScheduler'
