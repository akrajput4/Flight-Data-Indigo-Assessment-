import configparser

configs = configparser.ConfigParser()
configs.read('config.ini')
configs.sections()


class EnvironmentConfigs:
    db = configs['DATABASE']['db']
    dbName = configs['DATABASE']['dbName']
    dbHost = configs['DATABASE']['dbHost']
    dbPort = configs['DATABASE']['dbPort']
    dbUser = configs['DATABASE']['dbUser']
    dbPassword = configs['DATABASE']['dbPassword']

    broker_protocol = configs['CELERY']['broker_protocol']
    broker_username = configs['CELERY']['broker_username']
    broker_password = configs['CELERY']['broker_password']
    broker_host = configs['CELERY']['broker_host']
    broker_port = configs['CELERY']['broker_port']

    result_backend_protocol = configs['CELERY']['result_backend_protocol']
    result_backend_username = configs['CELERY']['result_backend_username']
    result_backend_password = configs['CELERY']['result_backend_password']
    result_backend_host = configs['CELERY']['result_backend_host']
    result_backend_port = configs['CELERY']['result_backend_port']
    result_backend_db = configs['CELERY']['result_backend_db']
    service_queue = configs['QUEUES']['service_queue']
