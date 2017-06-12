/**
 * Created by Administrator on 2017/4/19 0019.
 */

$(function(){
    $('#submit').click(function(event){
        event.preventDefault();
        var oldpasswordInput = $('input[name=old_password]');
        var newpasswordInput = $('input[name=new_password]');
        var newpasswordrepeatInput = $('input[name=new_password_repeat]');

        var oldpassword = oldpasswordInput.val();
        var newpassword = newpasswordInput.val();
        var newpasswordrepeat = newpasswordrepeatInput.val();

        xtajax.post({
            'url':'/modify_password/',
            'data':{
                'old_password':oldpassword,
                'new_password':newpassword,
                'new_password_repeat':newpasswordrepeat
            },
            'success':function(data){
                if(data['code']==200){
                    oldpasswordInput.val('');
                    newpasswordInput.val('');
                    newpasswordrepeatInput.val('');
                    xtalert.alertSuccessToast('恭喜您，修改成功');
                }else{
                    newpasswordInput.val('');
                    newpasswordrepeatInput.val('');
                    xtalert.alertInfoToast(data['message']);
                }
            },
            'fail':function(error){
                oldpasswordInput.val('');
                newpasswordInput.val('');
                newpasswordrepeatInput.val('');
                xtalert.alertNetworkError()
            }
        });
    });
});
