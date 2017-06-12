/**
 * Created by Administrator on 2017/5/26 0026.
 */
$(function () {
    var avatarImg = $('#avatar-img');
    xtqiniu.setUp({
        'browse_btn': 'avatar-img',
        'fileadded': function () {
            avatarImg.attr('alt','图片上传中...');
        },
        'success': function (up,file,info) {
            $('#avatar-img').attr('src',file.name);
        }
    });
});
$(function(){
    $('#submit-btn').click(function(event){
        event.preventDefault();
        var id = $(this).attr('data-user-id');
        var username = $('input[name="username"]').val();
        var realname = $('input[name="realname"]').val();
        var qq = parseInt($('input[name="qq"]').val());
        var email = $('input[name="email"]').val();
        var avatar = $('#avatar-img').attr('src');
        var signature = $('textarea[name="signature"]').val();
        var gender = parseInt($("input[type='radio']:checked").val());
        xtajax.post({
            'url':'/account/settings/',
            'data':{
                'username':username,
                'realname':realname,
                'qq':qq,
                'email':email,
                'avatar':avatar,
                'signature':signature,
                'id':id,
                'gender':gender
            },
            'success':function(data){
                if (data['code']==200){
                    xtalert.alertSuccessToast('恭喜，设置成功！');
                }else{
                    xtalert.alertInfoToast(data['message']);
                }
            }
        })
    })
});