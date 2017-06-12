#-*- coding:utf-8 -*-
from exts import db
from werkzeug.security import generate_password_hash,check_password_hash
import datetime,shortuuid
class GenderType(object):
    MAN = 1
    WOMAN = 2
    SECRET =3

class Regist(db.Model):
    __tablename__='front_user'
    id = db.Column(db.String(100),primary_key=True,default=shortuuid.uuid())
    username = db.Column(db.String(20),nullable=False)
    _password = db.Column(db.String(100),nullable=False)
    phone = db.Column(db.String(11),nullable=False)
    is_active = db.Column(db.Boolean,default=True)
    qq = db.Column(db.String(15))
    avatar =db.Column(db.String(100))
    join_time = db.Column(db.DateTime,default=datetime.datetime.now)
    last_login = db.Column(db.DateTime,nullable=True)
    old_last_login = db.Column(db.DateTime,nullable=True)
    email = db.Column(db.String(25),unique=True)
    gender = db.Column(db.Integer,default=GenderType.SECRET)
    realname = db.Column(db.String(30))
    signature = db.Column(db.String(150))
    points = db.Column(db.Integer,default=0)

    def __init__(self,username,phone,password):
        self.username = username
        self.password = password
        self.phone = phone

    @property
    def password(self):
        return self._password

    @password.setter
    def password(self,rawpwd):
        self._password = generate_password_hash(rawpwd)

    def check_password(self,rawpwd):
        return check_password_hash(self.password,rawpwd)
