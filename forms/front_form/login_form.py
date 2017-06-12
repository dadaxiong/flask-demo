#-*- coding:utf-8 -*-
from forms.baseform import BaseForm
from wtforms import StringField,IntegerField,DateField,ValidationError
from wtforms.validators import Length,InputRequired
from models.front_model.regist import Regist
from utils import xtcache

class Login(BaseForm):
    phone = StringField(validators=[Length(11,11,message=u'手机号码格式不正确'),InputRequired(message=u'手机号不能为空')])
    password = StringField(validators=[Length(6,100,message=u'密码格式不正确'),InputRequired(message=u'密码不能为空')])
    graph_captcha = StringField(validators=[Length(4,4,message=u'验证码格式不正确'),InputRequired(message=u'验证码不能为空')])
    remember = IntegerField()

    def validate_graph_captcha(self,field):
        graph_captcha = field.data
        che_graph_captcha = xtcache.get(graph_captcha)
        if not che_graph_captcha or graph_captcha.lower()!=che_graph_captcha.lower():
            raise ValidationError(message=u'图片验证码错误')
        return True