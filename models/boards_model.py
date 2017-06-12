#-*- coding:utf-8 -*-
from exts import db
import datetime

class Boards(db.Model):
    __tablename__='board'
    id = db.Column(db.Integer,primary_key=True,autoincrement=True)
    name = db.Column(db.String(100),nullable=False)
    create_time = db.Column(db.DateTime,default=datetime.datetime.now)
    author_id = db.Column(db.Integer,db.ForeignKey('user.id'))
    author = db.relationship('User',backref='boards')
