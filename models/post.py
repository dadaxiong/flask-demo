#-*- coding:utf8 -*-
from exts import db
import datetime
class Post(db.Model):
    id = db.Column(db.Integer,primary_key=True,autoincrement=True)
    title = db.Column(db.String(30),nullable=False)
    context = db.Column(db.Text,nullable=False)
    create_time = db.Column(db.DateTime,default=datetime.datetime.now)
    update_time = db.Column(db.DateTime,default=datetime.datetime.now,onupdate = datetime.datetime.now)
    read_count = db.Column(db.Integer,default= 0 )
    is_removed = db.Column(db.Boolean,default=False)

    author_id = db.Column(db.String(100),db.ForeignKey('front_user.id'))
    board_id = db.Column(db.Integer,db.ForeignKey('board.id'))
    highlight_id=db.Column(db.Integer,db.ForeignKey('highlight.id'))
    author = db.relationship('Regist',backref='posts')
    board = db.relationship('Boards',backref=db.backref('posts',lazy='dynamic'))
    highlights=db.relationship('Highlightmodel',backref='post',uselist=False)

class Highlightmodel(db.Model):
    __tablename__='highlight'
    id = db.Column(db.Integer,primary_key=True,autoincrement=True)
    create_time = db.Column(db.DateTime,default=datetime.datetime.now)

class Commentmodel(db.Model):
    __tablename__='comment'
    id = db.Column(db.Integer,primary_key=True,autoincrement=True)
    content = db.Column(db.Text,nullable=False)
    create_time = db.Column(db.DateTime,default=datetime.datetime.now)
    is_movie = db.Column(db.Boolean,default=False)

    post_id = db.Column(db.Integer,db.ForeignKey('post.id'))
    author_id = db.Column(db.String(100),db.ForeignKey('front_user.id'))
    origin_comment_id=db.Column(db.Integer,db.ForeignKey('comment.id'))

    post = db.relationship('Post',backref='comments')
    author = db.relationship('Regist',backref='comments')
    origin_comment = db.relationship('Commentmodel',backref='replys',remote_side=[id])

class PoststarsModel(db.Model):
    id = db.Column(db.Integer,primary_key=True,autoincrement=True)
    create_time = db.Column(db.DateTime,default=datetime.datetime.now)
    author_id = db.Column(db.String(100),db.ForeignKey('front_user.id'))
    post_id = db.Column(db.Integer,db.ForeignKey('post.id'))

    author = db.relationship('Regist',backref='stars')
    post = db.relationship('Post',backref='stars')