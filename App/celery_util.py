import time

from celery import Celery
from flask_mail import Message

from App.ext import mail
from manager import app


# 1.定义一个函数,用来在Flask里集成celery
def make_celery(app):
    celery = Celery("celery_util",broker="redis://localhost:6379")
    celery.conf.update(app.config)

    class ContextTask(celery.Task):
        def __call__(self, *args, **kwargs):
            with app.app_context():
                return self.run(*args, **kwargs)

    celery.Task = ContextTask
    return celery


# 2.调用make_celery方法  创建celery对象
celery = make_celery(app)


# 3.定义任务
@celery.task
def send_mail(subject,recipients,html):
    msg = Message()
    msg.subject = subject
    msg.recipients = recipients
    msg.html = html
    time.sleep(20)
    print("注册成功")
    mail.send(msg)

    # 还可以调用send_message方法，给定一系列的参数发送邮件,不需要创建msg对象
    # mail.send_message(subject=subject, recipients=recipients, html=html)


# 4. 启动celery的worker
# celery -A App.celery_util:celery worker --loglevel=info

