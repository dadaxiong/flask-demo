/**
 * Created by Administrator on 2017/4/24 0024.
 */
 $(function(){
    $('#submit').click(function(event){
        event.preventDefault();
        var usernameInput=$('input[name=username]');
        var passwordInput=$('input[name=password]');
        var emailInput = $('input[name=email]');
        var selectcheckbox = $(':checkbox:checked');

        var username= usernameInput.val();
        var password = passwordInput.val();
        var email = emailInput.val();
        var roles =[];
        selectcheckbox.each(function(index,element){
            var role_id = $(this).val();
            roles.push(role_id)
        });
        xtajax.post({
            'url':'/add_cmsuser/',
            'data':{
                'username':username,
                'password':password,
                'email':email,
                'roles':roles
            },
            'success':function(data){
                if(data['code']==200){
                    usernameInput.val('');
                    passwordInput.val('');
                    emailInput.val('');
                    selectcheckbox.each(function(){
                       $(this).prop('checked',false);
                    });
                    xtalert.alertSuccessToast('恭喜你，CMS用户已经添加成功！');
                }else{
                    xtalert.alertInfoToast(data['message']);
                }
            }
        })
    });
});