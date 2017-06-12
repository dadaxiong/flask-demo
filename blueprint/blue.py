#-*- coding:utf-8 -*-
from flask import views,request,redirect,render_template,url_for,session,g
from auth import login_required,super_adminnstator
from exits_blue import bp
from forms.form import LoginForm,ModifyPassword,ModifyEmail,Addcmsuser,PullBlack,Edit_boardForm,Delete_boardForm,HighlightForm
from models.cms_model import User,CMSRoles
from models.front_model.regist import Regist
from models.boards_model import Boards
from models.post import Post,Highlightmodel,Commentmodel
from task import celery_send_mail
import contants,flask
from exts import db
from utils import xtjson,send_email,xtcache
import string,random
from models.modelhelp import Helpmodel
class LoginView(views.MethodView):
    def get(self,massage=None):
        return render_template('cms/login.html', message=massage)
    def post(self):
        form = LoginForm(request.form)
        if form.validate():
            email =form.email.data
            password1 =form.password.data
            remeber =form.remeber.data
            user =User.query.filter_by(email = email).first()
            if user and user.check_user_password(password1):
                if not user.is_active:
                    return flask.abort(401)
                session[contants.USER_SESSION_ID] =user.id
                if remeber:
                    session.permanent = True
                else:
                    session.permanent = False
                return redirect(url_for('cms.index'))
            else:
                return self.get(massage=u'邮箱或密码错误')
        else:
            message = form.error_message()
            return self.get(massage=message)
bp.add_url_rule('/cms_login/',view_func=LoginView.as_view('login'))

@bp.route('/index/',methods=['GET','POST'])
@login_required
def index():
    return render_template('cms/index.html')

@bp.route('/loginout/')
@login_required
def loginout():
    session.pop(contants.USER_SESSION_ID)
    return redirect(url_for('cms.login'))

@bp.route('/person_center/')
@login_required
def person_center():
    return render_template('cms/person_center.html')

@bp.route('/modify_password/',methods=['GET','POST'])
@login_required
def modify_password():
    if request.method=='GET':
        return render_template('cms/modify_password.html')
    else:
        form = ModifyPassword(request.form)
        if form.validate():
            old_password = form.old_password.data
            new_password = form.new_password.data
            if g.cms_user.check_user_password(old_password):
                g.cms_user.password = new_password
                db.session.commit()
                return xtjson.json_result()
            else:
                return xtjson.json_params_error(u'密码错误')
        else:
            message = form.error_message()
            return xtjson.json_params_error(message)

@bp.route('/modify_email/',methods=['GET','POST'])
@login_required
def modify_email():
    if request.method == 'GET':
        return render_template('cms/modify_email.html')
    else:
        form = ModifyEmail(request.form)
        if form.validate():
            email = form.email.data
            # if flask.g.cms_user.email == email:
            #     return xtjson.json_params_error(u'俩次邮箱一致，无需修改')
            flask.g.cms_user.email=email
            db.session.commit()
            return xtjson.json_result()
        else:
            return xtjson.json_params_error(message=form.error_message())

@bp.route('/get_captcha/')
@login_required
def get_captcha():
    email =request.args.get('email')
    if xtcache.get(email):
        return xtjson.json_params_error(u'该邮箱已经发过验证码了')
    sorce = list(string.letters)
    for x in xrange(0,10):
        sorce.append(str(x))
    captcha_list=random.sample(sorce,6)
    captcha = ''.join(captcha_list)
    celery_send_mail.delay(subject=u'大熊论坛验证码',receviers=email,body=u'您本次的验证码是:'+captcha)
    return xtjson.json_result()


@bp.route('/cmsuser/')
@login_required
def cmsuser():
    users = User.query.all()
    context={
        'users':users
    }
    if request.method == 'GET':
        return render_template('cms/cmsuser.html', **context)

@bp.route('/add_cmsuser/',methods=['GET','POST'])
@super_adminnstator
@login_required
def add_cmsuser():
    if request.method == 'GET':
        roles = CMSRoles.query.all()
        context={
            'roles':roles
        }
        return render_template('cms/add_cmsuser.html', **context)
    else:
        username = request.form.get('username')
        password = request.form.get('password')
        email = request.form.get('email')
        roles = request.form.getlist('roles[]')
        form = Addcmsuser(request.form)
        if form.validate():
            user = User(username=username,password=password,email=email)
            if not roles:
                return xtjson.json_params_error(u'至少添加一个分组')
            for role_id in roles:
                role = CMSRoles.query.get(role_id)
                role.users.append(user)
            db.session.commit()
            return xtjson.json_result()
        else:
            return xtjson.json_params_error(message=form.error_message())

@bp.route('/edit_cmsuser/',methods=['GET','POST'])
@super_adminnstator
@login_required
def edit_cmsuser():
    if request.method =='GET':
        id = request.args.get('user_id')
        if id:
            user = User.query.get(id)
            roles = CMSRoles.query.all()
            current_id = [role.id for role in user.roles]
            context={
                'user':user,
                'roles':roles,
                'current_id':current_id
            }
            return render_template('cms/edit_cmsuser.html', **context)
        else:
            return flask.abort
    else:
        roles = request.form.getlist('roles[]')
        user_id = request.form.get('user_id')
        if not user_id:
            return xtjson.json_params_error(message=u'用户id不存在')
        if not roles:
            return xtjson.json_params_error(message=u'没有指定角色')
        user = User.query.get(user_id)
        user.roles[:]=[]
        for role in roles:
            role_model = CMSRoles.query.get(role)
            user.roles.append(role_model)
        db.session.commit()
        return xtjson.json_result()

@bp.route('/is_black/',methods=['POST'])
@super_adminnstator
@login_required
def is_black():
    form = PullBlack(request.form)
    if form.validate():
        user_id = form.user_id.data
        if user_id == flask.g.cms_user.id:
            return xtjson.json_params_error(message=u'用户不能拉黑自己')
        is_black = form.is_black.data
        user= User.query.get(user_id)
        user.is_active = not is_black
        db.session.commit()
        return xtjson.json_result()
    else:
        return xtjson.json_params_error(message=form.error_message())

@bp.route('/front_cms_user/')
@login_required
def front_cms_user():
    sort = request.args.get('sort')
    if not sort or sort == '1':
        front_cms_user = Regist.query.order_by(Regist.join_time.asc()).all()
    else:
        front_cms_user = Regist.query.all()
    content = {
        'front_user':front_cms_user,
        'current_sort':sort
    }
    return render_template('cms/front_cms_user.html',**content)

@bp.route('/edit_front_user/')
@login_required
def edit_front_user():
    user_id = request.args.get('user_id')
    if not user_id:
        flask.abort(401)
    front_cms_user = Regist.query.get(user_id)
    if not front_cms_user:
        flask.abort(404)
    return render_template('cms/edit_front_user.html',user=front_cms_user)

@bp.route('/black_front_user/',methods=['POST'])
@login_required
def black_front_user():
    form = PullBlack(request.form)
    user_id = form.user_id.data
    print user_id
    is_black = form.is_black.data
    user = Regist.query.get(user_id)
    if form.validate():
        user.is_active=not is_black
        db.session.commit()
        return xtjson.json_result()
    else:
        return xtjson.json_params_error(message=form.error_message())

@bp.route('/cms_boards/')
@login_required
def cms_boards():
    board = Boards.query.all()
    content={
        'boards':board
    }
    return render_template('cms/cms_boards.html',**content)

@bp.route('/add_board/',methods=['POST'])
@login_required
def add_board():
    author = request.form.get('author')
    board_name = request.form.get('name')
    if not board_name:
        return xtjson.json_params_error(message=u'添加的版块名称不能为空！')
    boardmodel = Boards.query.filter_by(name = board_name).first()
    if boardmodel:
        return xtjson.json_params_error(message=u'该版块已存在，无需添加！')
    board = Boards(name = board_name)
    author = User.query.filter_by(username=author).first()
    board.author=author
    db.session.commit()
    return xtjson.json_result()

@bp.route('/edit_board/',methods=['POST'])
@login_required
def edit_board():
    form = Edit_boardForm(request.form)
    if form.validate():
        board_id = form.board_id.data
        board_name = form.board_name.data
        boardmodel = Boards.query.get(board_id)
        boardmodel.name=board_name
        db.session.commit()
        return xtjson.json_result()
    else:
        return xtjson.json_params_error(message=form.error_message())

@bp.route('/delete_board/',methods=['POST'])
@login_required
def delete_board():
    form = Delete_boardForm(request.form)
    if form.validate():
        board_id = form.board_id.data
        print board_id
        boardmodel = Boards.query.filter_by(id=board_id).first()
        db.session.delete(boardmodel)
        db.session.commit()
        return xtjson.json_result()
    else:
        return xtjson.json_params_error(message=form.error_message())

@bp.route('/cms_post/')
@login_required
def cms_post():
    page = request.args.get('page',1,type=int)
    board_id = request.args.get('board',0,type=int)
    sort = request.args.get('sort',1,type=int)
    context = Helpmodel.helplist(page,sort,board_id)
    return render_template('cms/cms_post.html',**context)

@bp.route('/highlight/',methods=['POST'])
@login_required
def highlight():
    form = HighlightForm(request.form)
    post_id = form.post_id.data
    is_highlight = form.is_highlight.data
    if form.validate():
        postmodel = Post.query.get(post_id)
        if is_highlight:
            if postmodel.highlights:
                return xtjson.json_params_error(message=u'该帖子已经加过精了')
            else:
                highlightmodel = Highlightmodel()
                postmodel.highlights = highlightmodel
                db.session.commit()
                return xtjson.json_result()
        else:
            if not postmodel.highlights:
                return xtjson.json_params_error(message=u'该帖子无需取消加精')
            else:
                postmodel = postmodel.highlights
                db.session.delete(postmodel)
                db.session.commit()
                return xtjson.json_result()
    else:
        return xtjson.json_params_error(message=form.error_message())

@bp.route('/post_remove/',methods=['POST'])
@login_required
def post_remove():
    id = request.form.get('delete_post_id')
    if not id:
        return xtjson.json_params_error(message=u'必须输入帖子id')
    post_model = Post.query.get(id)
    post_model.is_removed = True
    db.session.commit()
    return xtjson.json_result()
@bp.context_processor
def cms_context_processor():
    id = session.get(contants.USER_SESSION_ID)
    if id:
        user = User.query.get(id)
        return {'cms_user':user}
    else:
        return {}

@bp.errorhandler(404)
def abort(error):
    return render_template('common/404.html'),404

@bp.errorhandler(401)
def abort(error):
    if request.is_xhr:
        return xtjson.json_unauth_error(message=u'你没有权限访问这个页面')
    return render_template('common/401.html'),401




