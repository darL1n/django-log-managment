# Django-Log-Managment

**Django-Log-Managment - сервис для администрирования и работы с логами**

# Обзор

Django-Log-Managment - это гибкий инструментарий для администрирования, мониторинга и ведения аналитики логов и действий пользователя.

----

# Требования

* Python 3.6+
* Django 4.1, 4.0, 3.2
* Djangorestframework >= 3.14.0

**Настоятельно рекомендуется** поддерживать только последние выпуски исправлений для каждой серии Python и Django.

## Монтаж

Установить используя `ssh`...
```bash
git clone git@github.com:darL1n/django-log-managment.git
```
## Настройка

В папке вашего проекта там же где и `settings.py` создайте новый файл `logconf.py` и поместите туда следующий код:

```python
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'main_format': {
            'format': '{levelno}\t{asctime}\t{module}\t{message}',
            'style': '{',
        },
        'traceback_format': {
            "format": "{levelno}\t{asctime}\t{message}",
            'style': '{'
        },

    },
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
            'formatter': 'main_format'
        },
        'file': {
            'class': 'logging.FileHandler',
            'formatter': 'main_format',
            'filename': 'logs.log'
        },
        'traceback_file': {
            'class': 'logging.FileHandler',
            'formatter': 'traceback_format',
            'filename': 'trace_logs.log'
        },
        
        
    },
    'loggers': {
        'main': {
            'handlers': ['console', 'file'],
            'level': 'INFO',
            'propagate': True
        },
        'trace': {
            'handlers': ['traceback_file'],
            'level': 'WARNING',
            'propagate': True
        },

    }
}

def replace_linesoferror(error):
    return error.replace('\n', '///')

PROJECT_NAME = 'НАЗВАНИЕ_ВАШЕГО_ПРОЕКТА'

LOG_SERVICE_URL = 'http://log-service-url/api/v1/'

```

И импортируйте данный файл в `settings.py` :

```python
from .logconf import LOGGING
```

В вашем проекте в `INSTALLED_APPS` должны быть установлены `rest_framework` и `corsheaders`

### Настройте `CORS` :

```python
CORS_ORIGIN_ALLOW_ALL = True
CSRF_TRUSTED_ORIGINS = ['']
```
## Использование
* Вся настройка производится в вашем проекте

Залогируем базовую страницу регистрации:

`views.py`
```python
import logging, traceback
from rest_framework.views import APIView
from backend.logconf import replace_linesoferror
from . import serializer

logger = logging.getLogger('main')
trace_logger = logging.getLogger('trace')

class SignUp(APIView):
    def post(self, request):
        try:
            user = User.objects.get(id=1000) # Вызовем ошибку чтобы записать traceback
        except:
            
            trace_logger.error(replace_linesoferror(traceback.format_exc())) # Обработаем обрывы строк

        serializer = serializers.SignUpUserSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        logger.info(f"Created new user: {serializer.data}") # Зарегестрируем действие
        return Response(serializer.data)


```

Ниже приведены примеры с ручной и автоматической выгрузкой логов:

### Ручная выгрузка

```python
def send_log_file():
    url = LOG_SERVICE_URL
    with open('logs.log', 'r+') as file:
        old_data = file.read()
        file.truncate(0)
        file.close()
    files = dict(file=old_data)
    data = dict(type=0, source_name=PROJECT_NAME)
    response = requests.post(url, files=files, data=data)

    return response


def send_trace_file():
    url = LOG_SERVICE_URL
    with open('trace_logs.log', 'r+') as file:
        old_data = file.read()
        file.truncate(0)
        file.close()
    files = dict(file=old_data)
    data = dict(type=1, source_name=PROJECT_NAME)
    response = requests.post(url, files=files, data=data)

    return response

send_log_file()
send_trace_file()

```

### Автоматическая выгрузка с использованием Celery и Redis (Рекомендуется)

Настройка Celery:

`settings.py`

```python
from celery.schedules import crontab

CELERY_BROKER_URL = 'redis://localhost:6379'
CELERY_RESULT_BACKEND = 'redis://localhost:6379'
CELERY_ACCEPT_CONTENT = ['application/json']
CELERY_IMPORTS = ['tasks']
CELERY_TASK_SERIALIZER = 'json'
CELERY_RESULT_SERIALIZER = 'json'
CELERY_TIMEZONE = TIME_ZONE

CELERY_BEAT_SCHEDULE = { 
    'Task_one_schedule' : {  
        'task': 'tasks.send_log_file', 
        'schedule': crontab(minute=0, hour=0), # crontab() runs the tasks every day in 00:00 
    },
    'Task_two_schedule' : {  
        'task': 'tasks.send_trace_file', 
        'schedule': crontab(minute=0, hour=0), # crontab() runs the tasks every day in 00:00 
    },
}
```

`celery.py`

```python
from __future__ import absolute_import, unicode_literals
import os
from django.conf import settings
from celery import Celery


os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'backend.settings')

app = Celery('backend')

app.config_from_object('django.conf:settings', namespace='CELERY')


app.autodiscover_tasks()
```

Terminal 1
```bash
celery -A backend.celery worker --loglevel=info -P solo
```
Terminal 2
```bash
celery -A backend beat -l debug
```
## Лицензия

[GNU](https://choosealicense.com/licenses/agpl-3.0/)
