/**
 * Created by Administrator on 2017/5/24 0024.
 */
$(function(){
    $('#star-btn').click(function(event){
        event.preventDefault();
        var post_id = $(this).attr('data-post-id');
        var is_star = parseInt($(this).attr('data-post-star'));
        var is_login_id = parseInt($(this).attr('data-login-id'));
        if (!is_login_id){
            window.location='/account/front_login/';
            return;
        }
        xtajax.post({
            'url':'/post/star_post/',
            'data':{
                'post_id':post_id,
                'is_star':!is_star
            },
            'success':function(data){
                if(data['code']==200){
                    var msg='';
                    if(is_star){
                        msg='该帖子已经取消点赞!';
                    }else{
                        msg='恭喜！帖子点赞成功!';
                    }
                    xtalert.alertSuccessToast(msg);
                    setTimeout(function(){
                        window.location.reload();
                    },500)
                }else{
                    xtalert.alertInfoToast(data['message']);
                }
            }
        })
    })
});