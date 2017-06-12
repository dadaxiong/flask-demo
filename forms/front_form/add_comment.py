#-*-coding:utf-8-*-
from forms.baseform import BaseForm
from wtforms import IntegerField,StringField,ValidationError,BooleanField
from wtforms.validators import InputRequired,Length
class AddcommentForm(BaseForm):
    post_id = IntegerField(validators=[InputRequired(message=u'必须指定一个帖子的id')])
    content = StringField(validators=[InputRequired(message=u'评论内容不能为空!')])
    origin_comment_id = IntegerField()

class StarpostForm(BaseForm):
    post_id = IntegerField(validators=[InputRequired(message=u'必须指定一个帖子id!')])
    is_star = BooleanField(validators=[InputRequired(message=u'必须输入点赞的行为!')])