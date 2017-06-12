# -*-coding:utf-8 -*-
import flask
from exts import db
from flask import Blueprint
from flask import redirect,request,render_template,url_for
from models.boards_model import Boards
from models.post import Post,Commentmodel,PoststarsModel,Highlightmodel
from forms.front_form.regist_form import Regist
from forms.front_form.Addpost_form import Addpost_form
from forms.front_form.add_comment import AddcommentForm,StarpostForm
import contants
import qiniu
from models.modelhelp import Helpmodel
from utils import xtjson,xtcache
from decorator.front_autr import login_required
bp = Blueprint('post',__name__,url_prefix='/post')

@bp.route('/')
def front_index():
    return front_list(1,1,0)

@bp.route('/front_list/<int:page>/<int:sort>/<int:board_id>')
def front_list(page,sort,board_id):
    context = Helpmodel.helplist(page,sort,board_id)
    return render_template('front/front_index.html',**context)

@bp.route('/post_detail/<int:post_id>/')
@login_required
def front_detail(post_id):
    postmodel = Post.query.filter(Post.is_removed==False,Post.id==post_id).first()
    if not postmodel:
        flask.abort(404)
    context={
        'post':postmodel,
        'star_author_ids':[star_model.author.id for star_model in postmodel.stars]
    }
    postmodel.read_count+=1
    db.session.commit()
    return render_template('front/front_postdetail.html',**context)

@bp.route('/add_comment/',methods=['GET','POST'])
@login_required
def add_comment():
    if request.method =='GET':
        post_id = request.args.get('post_id',type=int)
        comment_id = request.args.get('comment_id',type=int)
        context={
            'post':Post.query.get(post_id)
        }
        if comment_id:
            context['origin_comment'] = Commentmodel.query.get(comment_id)
        return render_template('front/front_addcomment.html',**context)
    else:
        form = AddcommentForm(request.form)
        if form.validate():
            id = form.post_id.data
            context = form.content.data
            comment_id = form.origin_comment_id.data
            commentmodel = Commentmodel(content = context)
            postmodel = Post.query.get(id)
            commentmodel.post = postmodel
            commentmodel.author = flask.g.front_user
            if comment_id:
                origin_comment = Commentmodel.query.get(comment_id)
                commentmodel.origin_comment = origin_comment
            commentmodel.author.points+=contants.ADDCOMMENT_POINTS
            db.session.add(commentmodel)
            db.session.commit()
            return xtjson.json_result()
        else:
            return xtjson.json_params_error(message=form.error_message())

@bp.route('/add_post/',methods=['GET','POST'])
@login_required
def add_post():
    if request.method=='GET':
        boards = Boards.query.all()
        return render_template('front/front_post.html',boards = boards)
    else:
        form = Addpost_form(request.form)
        if form.validate():
            title = form.title.data
            context = form.context.data
            board_id = form.board_id.data
            board = Boards.query.filter_by(id = board_id).first()
            if not board:
                return xtjson.json_params_error(message=u'该板块不存在')
            post = Post(title=title,context = context)
            post.author = flask.g.front_user
            post.board = board
            if post.author.points >= contants.ADDPOST_POINTS:
                db.session.add(post)
                db.session.commit()
                return xtjson.json_result()
            else:
                return xtjson.json_params_error(message=u'您的论坛积分未达到10分不能发表帖子!')
        else:
            return xtjson.json_params_error(message=form.error_message())

@bp.route('/star_post/',methods=['POST'])
@login_required
def star_post():
    form = StarpostForm(request.form)
    if form.validate():
        post_id = form.post_id.data
        is_star = form.is_star.data
        postmodel = Post.query.get(post_id)
        starpostmodel = PoststarsModel.query.filter_by(post_id = post_id,author_id = flask.g.front_user.id).first()
        if is_star:
            if starpostmodel:
                return xtjson.json_params_error(message=u'您已对该帖子已经点过赞！')
            starpostmodel = PoststarsModel()
            starpostmodel.author = flask.g.front_user
            starpostmodel.post = postmodel
            db.session.commit()
            return xtjson.json_result()
        else:
            if starpostmodel:
                db.session.delete(starpostmodel)
                db.session.commit()
                return xtjson.json_result()
            else:
                return xtjson.json_params_error(message=u'您还没有该帖子点赞，无需取消点赞操作')
    else:
        return xtjson.json_params_error(message=form.error_message())

 #设置七牛接口
@bp.route('/qiniu_token/')
def qiniu_token():
    q = qiniu.Auth(contants.QINIU_ACCESS_KEY,contants.QINIU_SECRET_KEY)
    bucket_name = 'daxiong'
    token = q.upload_token(bucket_name)
    return flask.jsonify({'uptoken':token})

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

@bp.errorhandler(401)
def post_auth_forbidden(error):
    if request.is_xhr:
        return xtjson.json_unauth_error()
    else:
        return redirect(url_for('account.front_login'))

@bp.errorhandler(404)
def page_auth_forbidden(error):
    if request.is_xhr:
        return xtjson.json_params_error()
    else:
        return render_template('common/404.html')


