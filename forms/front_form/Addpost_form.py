# -*-coding:utf-8 -*-
from forms.baseform import BaseForm
from wtforms import StringField,IntegerField,ValidationError
from wtforms.validators import InputRequired,Length
from utils import xtcache
class Addpost_form(BaseForm):
    title = StringField(validators=[InputRequired(message=u'帖子标题不能为空'),Length(1,30,message=u'标题长度在1-30个字符之间')])
    graph_captcha = StringField(validators=[InputRequired(message=u'验证码不能为空'),Length(4,4,message=u'验证码格式不正确')])
    context = StringField(validators=[InputRequired(message=u'发布内容不能为空！')])
    board_id = IntegerField(validators=[InputRequired(message=u'必须指定帖子板块ID')])

    def validate_graph_captcha(self,field):
        graph_captcha = field.data
        che_graph_captcha = xtcache.get(graph_captcha)
        if not che_graph_captcha or graph_captcha.lower()!=che_graph_captcha:
            raise ValidationError(message=u'验证码错误')
        return True