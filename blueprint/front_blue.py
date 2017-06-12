#-*- coding:utf-8 -*-
from flask import Blueprint,views,request,render_template
from exts import db
import flask
import contants,top,top.api
from forms.front_form.regist_form import Regist_form,SettingForm
from models.front_model.regist import Regist
from utils import xtjson,xtcache
from utils.captcha import xtcaptcha
from forms.front_form.login_form import Login
from datetime import datetime
from auth import front_user_required
captcha = xtcaptcha.Captcha
try:
    from StringIO import StringIO
except:
    from io import BytesIO as StringIO

bp = Blueprint('account',__name__,url_prefix='/account')

class Front_Login(views.MethodView):
    def get(self,message=None):
        return render_template('front/front_login.html',message=message)
    def post(self):
        form = Login(request.form)
        phone = form.phone.data
        password = form.password.data
        remember = form.remember.data
        if form.validate():
            front_user = Regist.query.filter_by(phone=phone).first()
            if front_user and front_user.check_password(password):
                flask.session[contants.FRONT_SESSION_ID] = front_user.id
                if front_user.old_last_login:
                    front_user.last_login = front_user.old_last_login
                front_user.old_last_login = datetime.now()
                if remember:
                    flask.session.permanent = True
                nowtime = datetime.now()
                last_login_time = front_user.last_login
                if not last_login_time or last_login_time.day != nowtime.day:
                    front_user.points += contants.LOGIN_POINTS
                    db.session.commit()
                return flask.redirect(flask.url_for('post.front_index'))
            else:
                return self.get(message=u'用户名或密码错误')
        else:
            return self.get(message=form.error_message())
bp.add_url_rule('/',view_func=Front_Login.as_view('front_login'))

class Front_Regist(views.MethodView):
    def get(self,message=None,**kwargs):
        context = {
            'message':message,
        }
        context.update(kwargs)
        return flask.render_template('front/front_regist.html',**context)
    def post(self):
        form = Regist_form(request.form)
        if form.validate():
            phone = form.phone.data
            username = form.username.data
            password = form.password.data
            user = Regist(username = username,password =password,phone = phone)
            db.session.add(user)
            db.session.commit()
            return render_template('front/front_login.html')
        else:
            username = request.form.get('username')
            password = request.form.get('password')
            password_repeat = request.form.get('password_repeat')
            phone = request.form.get('phone')
            return self.get(message=form.error_message(),username = username,password = password,phone=phone,password_repeat=password_repeat)
bp.add_url_rule('/regist/',view_func=Front_Regist.as_view('regist'))

@bp.route('/loginout/')
def loginout():
    flask.session.pop(contants.FRONT_SESSION_ID)
    return flask.redirect(flask.url_for('account.front_login'))

@bp.route('/settings/',methods=['GET','POST'])
@front_user_required
def setting():
    if request.method =='GET':
        return render_template('front/front_settings.html')
    else:
        form = SettingForm(request.form)
        if form.validate():
            id = form.id.data
            username = form.username.data
            realname = form.realname.data
            qq = form.qq.data
            avatar = form.avatar.data
            signature = form.signature.data
            email = form.email.data
            gender = form.gender.data
            user = Regist.query.filter_by(id = id).first()
            if id and user:
                user.qq = qq
                user.email=email
                user.realname = realname
                user.signature = signature
                user.gender = gender
                user.avatar=avatar
                user.username = username
                db.session.commit()
                return xtjson.json_result()
        else:
            return xtjson.json_params_error(message=form.error_message())
@bp.route('/main_page/<user_id>')
@front_user_required
def profile(user_id):
    if not user_id:
        return flask.abort(404)

    user = Regist.query.get(user_id)
    if user:
        context = {
            'current_user': user
        }
        return render_template('front/front_profile.html',**context)
    else:
        return flask.abort(404)
@bp.route('/profile_posts/')
@front_user_required
def profile_posts():
    user_id = flask.request.args.get('user_id')
    if not user_id:
        return flask.abort(404)
    user = Regist.query.get(user_id)
    if user:
        context = {
            'current_user': user,
        }
        return render_template('front/front_profile_posts.html',**context)
    else:
        flask.abort(404)

@bp.route('/send_message/')
def send_message():
    phone = request.args.get('phone')
    if not phone:
        return xtjson.json_params_error(message=u'必须指定一个手机号码')
    if xtcache.get(phone):
        return xtjson.json_params_error(message=u'验证码已发送，60秒内有效')

    app_key = contants.APP_KEY
    app_secret = contants.APP_SECRET
    req = top.setDefaultAppInfo(app_key,app_secret)
    req = top.api.AlibabaAliqinFcSmsNumSendRequest()
    req.extend=""
    req.sms_type='normal'
    req.sms_free_sign_name = contants.ALIDAYU_SIGN_NAME
    graph_captcha = captcha.gene_text()
    req.sms_param = "{code:%s}"% graph_captcha
    req.rec_num = phone.decode('utf-8').encode('ascii')
    req.sms_template_code = contants.ALIDAYU_TEMPLATE_CODE
    try:
        resp = req.getResponse()
        xtcache.set(phone,graph_captcha)
        print xtcache.get(graph_captcha)
        return xtjson.json_result()
    except Exception,e:
        print e
        return xtjson.json_server_error()

@bp.route('/graph_captcha/')
def graph_captcha():
    text,image = captcha.gene_code()
    # StringIO相当于是一个管道
    out = StringIO()
    # 把image塞到StingIO这个管道中
    image.save(out,'png')
    # 将StringIO的指针指向开始的位置
    out.seek(0)
    # 生成一个响应对象，out.read是把图片流给读出来
    response = flask.make_response(out.read())
    # 指定响应的类型
    response.content_type = 'image/png'
    xtcache.set(text.lower(),text.lower(),timeout=60)
    return response
@bp.before_request
def post_before_request():
    id = flask.session.get(contants.FRONT_SESSION_ID)
    if id:
        user = Regist.query.get(id)
        flask.g.front_user = user

@bp.context_processor
def post_context_processor():
    if hasattr(flask.g,'front_user'):
        return {'front_user':flask.g.front_user}
    else:
        return {}
