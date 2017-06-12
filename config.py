#-*- coding:utf8 -*-
import os
from datetime import timedelta
SERVER_NAME='daxiong.com:8000'
PERMANENT_SESSION_LIFETIME = timedelta(days=5)
HOST='127.0.0.1'
PORT=3306
USERNAME = 'root'
DATABASE = 'daxiong'
CHARSET ='utf-8'
DB_URI='mysql+mysqldb://{}@{}:{}/{}?{}'.format(USERNAME,HOST,PORT,DATABASE,CHARSET)
SQLALCHEMY_DATABASE_URI = DB_URI
SQLALCHEMY_TRACK_MODIFICATIONS=False
SECRET_KEY= os.urandom(24)

MAIL_SERVER = 'smtp.qq.com'
MAIL_PORT = '587'
MAIL_USERNAME='1817864124@qq.com'
MAIL_PASSWORD='gdnjlifbqmbyeijg'
MAIL_DEFAULT_SENDER='1817864124@qq.com'
MAIL_USE_TLS= True