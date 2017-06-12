#-*- coding:utf-8 -*-
from forms.baseform import BaseForm
from wtforms import IntegerField,StringField,ValidationError
from wtforms.validators import InputRequired,Regexp,EqualTo,Length,Email,URL
from models.front_model.regist import Regist
from utils import xtcache
class Regist_form(BaseForm):
    username = StringField(validators=[Length(6,20,message=u'用户名长度在6-20个字符之间'),InputRequired(message=u'用户名不能为空')])
    password = StringField(validators=[Length(6,20,message=u'密码长度6-20个字符之间'),InputRequired(message=u'密码不能为空')])
    password_repeat = StringField(validators=[EqualTo('password',message=u'俩次密码必须一致')])
    phone = StringField(validators=[Regexp('(\d{11})|^((\d{7,8})|(\d{4}|\d{3})-(\d{7,8})|(\d{4}|\d{3})-(\d{7,8})-(\d{4}|\d{3}|\d{2}|\d{1})|(\d{7,8})-(\d{4}|\d{3}|\d{2}|\d{1}))$'),InputRequired(message=u'电话号码不能为空')])
    phone_captcha = StringField(validators=[InputRequired(message=u'手机验证码必须输入')])
    graph_captcha = StringField(validators=[InputRequired(message=u'验证码必须输入')])

    def validate_phone(self,field):
        phone = field.data
        if phone== '18888888888':
            raise ValidationError(u'该手机号不能被注册')
        phone_ed = Regist.query.filter_by(phone = phone).first()
        if phone_ed:
            raise ValidationError(u'该手机已经注册')
        return True

    def validate_username(self,field):
        username = field.data
        username_ed =Regist.query.filter_by(username = username).first()
        if username_ed:
            raise ValidationError(u'该用户名已经存在')
        return True

    def validate_phone_captcha(self,field):
        phone_captcha = field.data
        phone = self.phone.data
        message = xtcache.get(phone)
        if not message or message.lower()!= phone_captcha.lower():
            raise ValidationError(message=u'手机短信验证码错误')
        return True

    def validate_graph_captcha(self,field):
        graph_captcha = field.data
        cache_graph_captcha = xtcache.get(graph_captcha.lower())
        if not cache_graph_captcha or graph_captcha.lower()!= cache_graph_captcha.lower():
            raise ValidationError(message=u'图形验证码错误！')
        return True
class SettingForm(BaseForm):
    realname = StringField(validators=[Length(1,10,message=u'真实姓名长度在1-10个字符之间')])
    qq = StringField(validators=[Length(6,10,message=u'qq号码格式不正确')])
    email = StringField(validators=[Email(message=u'邮箱格式输入不正确')])
    avatar = StringField(validators=[URL(message=u'图片地址错误')])
    id = StringField(validators=[InputRequired(message=u'用户id不能为空')])
    signature = StringField(validators=[Length(1,50,message=u'长度在50个字符以内')])
    username = StringField(validators=[Length(1,20,message=u'用户名长度在1-20个字符之间'),InputRequired(message=u'用户名不能为空')])
    gender = IntegerField()