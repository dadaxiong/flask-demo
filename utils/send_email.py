#-*- coding:utf8 -*-
from flask_mail import Message
from exts import mail
def send_email(subject,receviers,body=None,html=None):
    #断言必须要有接受者
    assert receviers
    #如果发送的邮件没有内容
    if not body and not html:
        return False
    if isinstance(receviers,str) or isinstance(receviers,unicode):
        receviers = [receviers]
    message = Message(subject=subject,recipients=receviers,body=body,html=html)
    try:
        mail.send(message)
    except:
        return False
    return True


