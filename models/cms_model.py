#-*- coding:utf-8 -*-
import datetime
from exts import db
from werkzeug.security import generate_password_hash,check_password_hash

class CMSPermission(object):
    ADMINISTRATOR = 255
    OPERASTOR = 1
    MIDDLEOPEATER = 4
    HIGHSTRATOR = 64
    PERMISSION_MAP = {
        ADMINISTRATOR:(u'超级管理员权限',u'拥有至高无上的权利'),
        HIGHSTRATOR:(u'高级管理员',u'拥有管理模块的权利'),
        OPERASTOR:(u'普通管理员',u'可以操作前台用户，帖子等'),
        MIDDLEOPEATER:(u'中低级管理员',u'可以操作帖子评论的权限')
    }
cms_user_role = db.Table('cms_user_role',
    db.Column('user_id',db.Integer,db.ForeignKey('user.id'),primary_key=True),
    db.Column('cmsrole_id',db.Integer,db.ForeignKey('cmsroles.id'),primary_key=True))
class CMSRoles(db.Model):
    __tablename__ = 'cmsroles'
    id = db.Column(db.Integer,primary_key=True,autoincrement=True)
    settime = db.Column(db.DateTime,default=datetime.datetime.now)
    name = db.Column(db.String(100),nullable=False)
    desc = db.Column(db.String(100),nullable=True)
    permissions = db.Column(db.Integer,default=CMSPermission.OPERASTOR,nullable=False)
    users = db.relationship('User',secondary = cms_user_role)
class User(db.Model):
    __tablename__ = 'user'
    id = db.Column(db.Integer,primary_key=True,autoincrement=True)
    username = db.Column(db.String(30))
    _password = db.Column(db.String(100))
    email = db.Column(db.String(30))
    datetime = db.Column(db.DateTime,default=datetime.datetime.now)
    last_login_time = db.Column(db.DateTime,nullable=True)
    is_active = db.Column(db.Boolean,default=True)
    roles = db.relationship('CMSRoles',secondary=cms_user_role)

    def __init__(self,username,password,email):
        self.username=username
        self.password=password
        self.email =email

    @property
    def password(self):
        return self._password

    @password.setter
    def password(self,rawpwd):
        self._password = generate_password_hash(rawpwd)

    def check_user_password(self,rawpwd):
        return check_password_hash(self.password,rawpwd)

    def has_permission(self,permission):
        if not self.roles:
            return False
        else:
            all_permissions = 0
            for role in self.roles:
                all_permissions |=role.permissions
            return all_permissions & permission == permission

    @property
    def superadministrator(self):
        return self.has_permission(CMSPermission.ADMINISTRATOR)

    @property
    def permissions(self):
        if not self.roles:
            return None

        all_permisssion = 0
        for role in self.roles:
            all_permisssion|=role.permissions

        permission_dict = []
        for permission,permisson_info in CMSPermission.PERMISSION_MAP.iteritems():
            if all_permisssion & permission ==permission:
                permission_dict.append({permission:permisson_info})
        return permission_dict









