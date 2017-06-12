#-*-coding:utf-8-*-
from celery import Celery,Task
from utils import send_email
from exts import app
def make_celery(app):
    celery = Celery(app.import_name, backend='redis://:daxiong@192.168.223.129:6379/1',
                    broker='redis://:daxiong@192.168.223.129:6379/1')
    TaskBase = celery.Task
    class ContextTask(TaskBase):
        abstract = True
        def __call__(self,*args,**kwargs):
            with app.app_context():
                return TaskBase.__call__(self,*args,**kwargs)
    celery.Task = ContextTask
    return celery
celery = make_celery(app)
@celery.task
def celery_send_mail(subject,receviers,body=None,html=None):
    with app.app_context():
        send_email.send_email(subject,receviers,body,html)