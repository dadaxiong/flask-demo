#! /use/bin/env python
#-*-coding:utf-8-*-
import os
import sys
reload(sys)
sys.setdefaultencoding('gb18030')
import datetime
from blueprint import blue,front_blue,post
from flask_wtf import CsrfProtect
from exts import app
app.register_blueprint(blue.bp)
app.register_blueprint(front_blue.bp)
app.register_blueprint(post.bp)
CsrfProtect(app)

@app.template_filter('handler_time')
def handler_time(time):
    if type(time)==datetime.datetime:
        now = datetime.datetime.now()
        tmptime = (now-time).total_seconds()
        if tmptime < 60:
            return u'刚刚'
        elif 60 <= tmptime and tmptime<60*60:
            minutes = tmptime / 60
            return u'%s分钟前'% int(minutes)
        elif 60*60 <=tmptime and tmptime <60*60*24:
            hours = tmptime / (60*60)
            return u'%s小时前'%int(hours)
        elif 60*60*24<=tmptime and tmptime < 60*60*24*30:
            days = tmptime / (60*60*24)
            return u'%s天前'%int(days)
        elif now.year == time.year:
            return time.strftime('%m-%d %H:%M:%S')
        else:
            return time.strftime('%Y-%m-%d %H:%M:%S')
    return time

if __name__ == '__main__':
    app.run(host='0.0.0.0')

