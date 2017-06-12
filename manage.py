#-*- coding:utf8 -*-
from exts import app,db
from flask_migrate import MigrateCommand,Migrate
from flask_script import Manager
from models import cms_model
from models.front_model import regist
from models.boards_model import Boards
from models.post import Post,Commentmodel,Highlightmodel,PoststarsModel
User =cms_model.User
Front_user = regist.Regist
from werkzeug.security import generate_password_hash
manager = Manager(app)
migrate= Migrate(app,db)
manager.add_command('db',MigrateCommand)

@manager.option('-u','--username',dest='username')
@manager.option('-p','--password',dest='password')
@manager.option('-e','--email',dest='email')
@manager.option('-r','--role_name',dest='role_name')
def create_user(username,password,email,role_name):
    use =User.query.filter_by(email =email).first()
    role_name = cms_model.CMSRoles.query.filter_by(name=role_name.decode('gbk').encode('utf8')).first()
    if not use:
        if role_name:
            user =User(username =username.decode('gbk').encode('utf8'),email=email,password=password)
            role_name.users.append(user)
            db.session.commit()
            print u'恭喜，该用户已经添加成功'

@manager.option('-n','--name',dest='name')
@manager.option('-d','--desc',dest='desc')
@manager.option('-p','--permission',dest='permission')
def create_role(name,desc,permission):
    role_model = cms_model.CMSRoles(name = name.decode('gbk').encode('utf8'),desc=desc.decode('gbk').encode('utf8'),permissions=permission)
    db.session.add(role_model)
    db.session.commit()
    print u'恭喜，角色添加成功！'

@manager.option('-u','--username',dest='username')
@manager.option('-p','--password',dest='password')
@manager.option('-t','--telephone',dest='telephone')
def create_front_user(username,password,telephone):
    front_user = Front_user(username=username.decode('gbk').encode('utf8'),password=password,phone=telephone)
    db.session.add(front_user)
    db.session.commit()
    print  u'恭喜，前台用户添加成功！'

@manager.option('-n','--name',dest='name')
@manager.option('-i','--id',dest='id')
def create_board(name,id):
    board = Boards(name=name.decode('gbk').encode('utf8'),author_id = id)
    db.session.add(board)
    db.session.commit()
    print u'恭喜！模块添加成功！'

if __name__ =='__main__':
    manager.run()