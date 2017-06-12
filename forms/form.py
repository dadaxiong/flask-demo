#-*- coding:utf-8 -*-
import flask
from baseform import BaseForm
from wtforms import StringField,IntegerField,ValidationError,BooleanField
from wtforms.validators import EqualTo,Email,Length,required,InputRequired
from models.cms_model import User
from utils import xtcache
class LoginForm(BaseForm):
    id =IntegerField ()
    email = StringField(validators=[Email(message=u'邮箱格式不正确'),InputRequired(message=u'邮箱必须输入')])
    password = StringField(validators=[Length(6,20,message=u'密码长度必须在6-20之间'),InputRequired(message=u'密码必须输入')])
    remeber = BooleanField()
    # def email_required(self,field):
    #     email = field.data
    #     user = User.query.filter_by(email = email).first()
    #     if user:
    #         raise ValueError( u'该邮箱已注册,不能重复注册！')

class ModifyPassword(BaseForm):
    old_password = StringField(validators=[Length(6,20,message=u'原始密码长度在6-20之间'),InputRequired(message=u'原始密码必须输入')])
    new_password = StringField(validators=[Length(6,20,message=u'新密码长度在6-20之间'),InputRequired(message=u'设置的新密码必须输入')])
    new_password_repeat = StringField(validators=[EqualTo('new_password',message=u'俩次设置的新密码必须一致'),InputRequired(message=u'确认的新密码必须填写')])

class ModifyEmail(BaseForm):
    email = StringField(validators=[Email(message=u'邮箱格式不正确'),InputRequired(message=u'邮箱必须输入')])
    captcha = StringField(validators=[InputRequired(message=u'验证码不能为空')])

    def email_validators(self,field):
        email = field.email.data
        chache_email = xtcache.cache.get(email)
        captcha = field.data
        if not captcha or chache_email.lower()!=email:
            return False
        return True

class Addcmsuser(BaseForm):
    password = StringField(validators=[Length(6,20,message=u'长度在6-20之间'),InputRequired(message=u'密码不能为空')])
    username = StringField(validators=[Length(6,20,message=u'长度在6-20之间'),InputRequired(message=u'用户名必须输入')])
    email = StringField(validators=[Email(message=u'邮箱格式不正确'),InputRequired(message=u'邮箱不能为空')])

class PullBlack(BaseForm):
    user_id = StringField(validators=[InputRequired(message=u'指定id不能为空')])
    is_black = IntegerField(validators=[InputRequired(message=u'此项不能为空')])

class Delete_boardForm(BaseForm):
    board_id = IntegerField(validators=[InputRequired(message=u'必须指定一个版块id')])

class Edit_boardForm(Delete_boardForm):
    board_name = StringField(validators=[InputRequired(message=u'编辑的版块名称真不能为空')])

class HighlightForm(BaseForm):
    post_id = IntegerField(validators=[InputRequired(message=u'必须指定一个帖子id')])
    is_highlight = BooleanField(validators=[InputRequired(message=u'加精项不能为空')])