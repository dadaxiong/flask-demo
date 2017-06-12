/**
 * Created by Administrator on 2017/4/26 0026.
 */
$(function(){
   $('#submit').click(function(event){
       event.preventDefault();
       var checkboxInput = $(':checkbox:checked');
       var roles =[];
       checkboxInput.each(function(){
           var role_id = $(this).val();
           roles.push(role_id);
       });
       var user_id = $(this).attr('data-user-id');
       xtajax.post({
            'url':'/edit_cmsuser/',
            'data':{
                'user_id':user_id,
                'roles':roles
            },
           'success': function (data) {
               if(data['code']==200){
                   xtalert.alertSuccessToast('恭喜，修改成功！')
               }else{
                   xtalert.alertErrorToast(data['message'])
               }
           }
       })
   })
});

$(function(){
    $('#black').click(function(event){
        event.preventDefault();

        var user_id = $(this).attr('data-user-id');
        var is_active = parseInt($(this).attr('data-is-active'));
        var is_black = is_active;
        xtajax.post({
            'url':'/is_black/',
            'data':{
                'user_id':user_id,
                'is_black':is_black
            },
            'success':function(data){
                if(data['code']==200){
                    var msg ='';
                    if(is_black){
                        msg = '该用户已拉入黑名单';
                    }else{
                        msg='该用户已移除黑名单';
                    }
                    xtalert.alertSuccessToast(msg);
                    setTimeout(function(){
                        window.location.reload();
                    },500);
                }else{
                    xtalert.alertErrorToast(data['message']);
                }
            }
        })
    })
});