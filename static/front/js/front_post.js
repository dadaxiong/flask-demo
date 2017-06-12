/**
 * Created by Administrator on 2017/5/7 0007.
 */
$(function(){
    $("#submit").click(function(event){
        event.preventDefault();
        var titleInput = $('input[name=title]');
        var graph_captchaInput = $('input[name=graph_captcha]');
        var title = titleInput.val();
        var graph_captcha = graph_captchaInput.val();
        var context = window.editor.$txt.html();
        var board_id = $('.board-select').val();

        xtajax.post({
            'url':'/post/add_post/',
            'data':{
                'title':title,
                'context':context,
                'board_id':board_id,
                'graph_captcha':graph_captcha
            },
            'success':function(data){
                if(data['code']==200){
                    xtalert.alertConfirm({
                        'msg':'恭喜！帖子发表成功',
                        'cancelText':'返回首页',
                        'confirmText':'在发表一篇',
                        'cancelCallback':function(){
                            window.location= '/post/';
                        },
                        'confirmCallback':function(){
                            titleInput.val('');
                            window.editor.clear();
                            graph_captchaInput.val('');
                            $('#graph-captcha-btn').click();
                        }
                    });
                }else{
                    xtalert.alertInfoToast(data['message']);
                    $('#graph-captcha-btn').click();
                }
            }
        })
    });
});
