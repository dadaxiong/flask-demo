/**
 * Created by Administrator on 2017/5/5 0005.
 */
$(function(){
    $('#is_black_btn').click(function(event){
        event.preventDefault();
        var user_id = $(this).attr('data-user-id');
        console.log(user_id);
        var is_active = parseInt($(this).attr('data-is-active'));
        var is_black = is_active;
        xtajax.post({
            'url':'/black_front_user/',
            'data':{
                'user_id':user_id,
                'is_black':is_black
            },
            'success':function(data){
                if(data['code']==200){
                    var msg='';
                    if (is_black){
                        msg = '该用户已加入黑名单';
                    }else{
                        msg='该用户已移除黑名单';
                    }
                    xtalert.alertSuccessToast(msg);
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