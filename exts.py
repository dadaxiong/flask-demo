#-*- coding:utf8 -*-
from flask_sqlalchemy import SQLAlchemy
from flask_mail import Mail
from flask import Flask
import config
app = Flask('luntan')
app.config.from_object(config)
db = SQLAlchemy(app)
mail = Mail(app)