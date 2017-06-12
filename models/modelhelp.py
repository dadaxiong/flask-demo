#-*-coding:utf-8 -*-
from models.boards_model import Boards
from models.post import Post,Commentmodel,Highlightmodel,PoststarsModel
import contants
from exts import db
class Helpmodel(object):
    class Sortlist(object):
        NEW_POST = 1
        STAR_POST = 2
        HIGH_POST = 3
        COMMENT_POST = 4
    @classmethod
    def helplist(cls,page,sort,board_id):
        if sort == cls.Sortlist.NEW_POST:
            posts = Post.query.order_by(Post.create_time.desc())
        elif sort == cls.Sortlist.STAR_POST:
            posts = db.session.query(Post).outerjoin(PoststarsModel).group_by(Post.id).order_by(PoststarsModel.create_time.desc(),Post.create_time.desc())
        elif sort == cls.Sortlist.HIGH_POST:
            posts = db.session.query(Post).outerjoin(Highlightmodel).group_by(Post.id).order_by(db.func.count(Highlightmodel.id).desc(),Post.create_time.desc())
        elif sort == cls.Sortlist.COMMENT_POST:
            posts = db.session.query(Post).outerjoin(Commentmodel).group_by(Post.id).order_by(db.func.count(Commentmodel.id).desc(),Post.create_time.desc())
        else:
            posts = Post.query.filter(Post.create_time.desc())
        if board_id !=0:
            posts = posts.filter(Post.board_id==board_id)
        posts = posts.filter(Post.is_removed==False)
        t_posts = posts.count()
        start = (page-1)*contants.PAGE_NUM
        end = start + contants.PAGE_NUM
        #先算出帖子有多少页
        page_list_total = t_posts/contants.PAGE_NUM
        if t_posts % contants.PAGE_NUM > 0:
            page_list_total +=1

        page_list_tmp=[]
        page_list = page -1
        while page_list >=1:
            if page_list % 5 ==0:
                break
            page_list_tmp.append(page_list)
            page_list-=1

        page_list = page
        while page_list <= page_list_total:
            if page_list % 5 ==0:
                page_list_tmp.append(page_list)
                break
            else:
                page_list_tmp.append(page_list)
                page_list+=1
        page_list_tmp.sort()

        context = {
            'boards':Boards.query.all(),
            'posts':posts.slice(start,end),
            'page_total':page_list_total,
            'page_list':page_list_tmp,
            'page':page,
            'c_sort':sort,
            'c_board':board_id,
            't_post_count':Post.query.filter_by(is_removed=False).count()
        }
        return context