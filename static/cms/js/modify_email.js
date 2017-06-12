/**
 * Created by Administrator on 2017/4/20 0020.
 */
$(function(){
    $('.input-group-addon').click(function(event){
       event.preventDefault();
        var emailInput = $('input[name=email]');
        var email_value = emailInput.val();
        xtajax.get({
           'url':'/get_captcha/',
           'data':{
                'email':email_value
           },
           'success':function(data){
               if (data['code']==200){
                   xtalert.alertSuccessToast();
               }else{
                   xtalert.alertErrorToast(data['message']);
               }
           },
           'fail':function(error){
               xtalert.alertNetworkError();
            }
        })
    });
    $('#submit').click(function(event){
        event.preventDefault();
        var emailInput = $('input[name=email]');
        var email_value = emailInput.val();
        var captcha = $('input[name=captcha]');
        var captcha_value = captcha.val();
        xtajax.post({
            'url':'/modify_email/',
            'data':{
                'email':email_value,
                'captcha':captcha_value
            },
            'success':function(data){
                if (data['code']==200){
                    xtalert.alertSuccessToast('恭喜，邮箱修改成功！');
                    emailInput.val('');
                    captcha.val('');
                }else{
                    captcha.val('');
                    xtalert.alertInfoToast(data['message']);
                }
            },
            'fail':function(error){
                xtalert.alertNetworkError()
            }

        })
    })
});