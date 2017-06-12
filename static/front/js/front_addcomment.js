/**
 * Created by Administrator on 2017/5/23 0023.
 */
$(function(){
    $('#submit-btn').click(function(event){
        event.preventDefault();
        var post_id = $(this).attr('data-post-id');
        var content = window.editor.$txt.html();
        var comment_id = $('.origin_comment_group').attr('data-origin-id');
        xtajax.post({
            'url':'/post/add_comment/',
            'data':{
                'post_id':post_id,
                'content':content,
                'origin_comment_id':comment_id
            },
            'success':function(data){
                if(data['code']==200){
                    xtalert.alertSuccessToast('恭喜,评论发表成功!');
                    setTimeout(function(){
                        window.location='/post/post_detail/'+post_id+'/';
                    },800)
                }else{
                    xtalert.alertInfoToast(data['message']);
                }
            }
        })
    })
});