/**
 * Created by Administrator on 2017/5/2 0002.
 */
$(function(){
   $('#phone_message').click(function(event){
       event.preventDefault();
       self = $(this);
       var phone = $('input[name=phone]').val();
       if(!phone){
           xtalert.alertErrorToast('请指定手机号码')
       }
       xtajax.get({
           'url':'/account/send_message/',
           'data':{
               'phone':phone
           },
           'success':function(data){
               if(data['code']==200){
                   xtalert.alertSuccessToast('恭喜你，验证码发送成功！');
                    var timeout = 60;
                    self.attr('disabled','disabled');
                    self.css('cursor','default');
                    var timer = setInterval(function(){
                        self.text(timeout);
                        timeout--;
                        if(timeout<=0){
                            self.text('发送验证码');
                            self.removeAttr('disabled');
                            clearInterval(timer);
                            self.css('cursor','pointer');
                        }
                    },1000);
               }else{
                   xtalert.alertInfoToast(data['message']);
               }
           }
       });
   });
});
