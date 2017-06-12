/**
 * Created by Administrator on 2017/5/22 0022.
 */
$(function(){
    $('.highlight-btn').click(function(event){
        event.preventDefault();
        var id = $(this).attr('data-post-id');
        var highlight = parseInt($(this).attr('data-is-highlight'));
        xtajax.post({
            'url':'/highlight/',
            'data':{
                'post_id':id,
                'is_highlight':!highlight
            },
            'success':function(data){
                if(data['code']==200){
                    msg='';
                    if(highlight){
                        msg='该帖子取消加精成功!';
                    }else{
                        msg='该帖子加精成功!';
                    }
                    xtalert.alertSuccessToast(msg);
                    setTimeout(function(){
                        window.location.reload();
                    },800)
                }else{
                    xtalert.alertErrorToast(data['message'])
                }
            }
        })
    })
});

$(function(){
    $('#delete-post').click(function(event){
        event.preventDefault();
        id = $(this).attr('data-post-id');
        xtajax.post({
            'url':'/post_remove/',
            'data':{
                'delete_post_id':id
            },
            'success':function(data){
                if(data['code']==200){
                    xtalert.alertSuccessToast('恭喜！该帖子删除成功!');
                    setTimeout(function(){
                        window.location.reload();
                    },800)
                }else{
                    xtalert.alertErrorToast(data['message']);
                }
            }
        })
    })
});

//路径排序
$(function(){
    $('#left-select').change(function(event){
        var value = $(this).val();
        var newHref = xtparam.setParam(window.location.href,'sort',value);
        window.location = newHref;
    })
});

$(function(){
    $('#board-filter-select').change(function(event){
        var value = $(this).val();
        var newHref = xtparam.setParam(window.location.href,'board',value);
        var newHref = xtparam.setParam(newHref,'page',1);
        window.location = newHref;
    })
});