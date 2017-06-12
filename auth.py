#-*-coding:utf8 -*-
from models.cms_model import User
from models.front_model.regist import Regist
import flask
from functools import wraps
import contants
from utils import xtjson
from models.cms_model import CMSPermission
def login_required(func):
    @wraps(func)
    def warpper(*args,**kwargs):
        id=flask.session.get(contants.USER_SESSION_ID)
        user =User.query.filter_by(id =id)
        if user and id:
            return func(*args,**kwargs)
        else:
            return flask.redirect(flask.url_for('cms.login'))
    return warpper
def front_user_required(func):
    @wraps(func)
    def wrapper(*args,**kwargs):
        user_id = flask.session.get(contants.FRONT_SESSION_ID)
        user = Regist.query.filter_by(id=user_id)
        if user_id and user:
            return func(*args,**kwargs)
        else:
            return flask.redirect(flask.url_for('account.front_login'))
    return wrapper

def permission(permission):
    def permission_required(func):
        @wraps(func)
        def warpper(*args,**kwargs):
            if flask.g.cms_user.has_permission(permission):
                return func(*args,**kwargs)
            else:
                return flask.abort(401)
        return warpper
    return permission_required

def super_adminnstator(func):
    return permission(CMSPermission.ADMINISTRATOR)(func)




