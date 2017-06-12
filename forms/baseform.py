#-*- coding:utf-8 -*-
from flask_wtf import FlaskForm

class BaseForm(FlaskForm):
    def error_message(self):
        _,values = self.errors.popitem()
        message = values[0]
        return message
