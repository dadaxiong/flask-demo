/**
 * Created by Administrator on 2017/5/11 0011.
 */
$(function() {
    $('#add-board-btn').click(function (event) {
        var author = $(this).attr('data-board-author');
        event.preventDefault();
        xtalert.alertOneInput({
            'text': '新的板块名称',
            'placeholder': '新版块名称',
            'confirmCallback': function(inputValue){
                xtajax.post({
                    'url': '/add_board/',
                    'data': {
                        'author': author,
                        'name': inputValue
                    },
                    'success': function (data) {
                        if (data['code'] == 200){
                            xtalert.alertSuccessToast('恭喜，板块添加成功');
                            setTimeout(function () {
                                window.location.reload();
                            },800)
                        } else {
                            xtalert.alertErrorToast(data['message'])
                        }
                    }
                })
            }
        })
    });
});
$(function() {
    $('.edit-board-btn').click(function(event){
        event.preventDefault();
        var board_id = $(this).attr('data-board-id');
        xtalert.alertOneInput({
            'text': '编辑新版块的名称',
            'placeholder': '新版块名称',
            'confirmCallback':function (inputValue){
                xtajax.post({
                    'url': '/edit_board/',
                    'data':{
                        'board_id':board_id,
                        'board_name':inputValue
                    },
                    'success': function (data) {
                        if (data['code'] == 200) {
                            xtalert.alertSuccessToast('恭喜，板块名称编辑完成！');
                            setTimeout(function (){
                                window.location.reload();
                            }, 800)
                        } else {
                            xtalert.alertErrorToast(data['message']);
                        }
                    }
                })
            }
        })
    });
});
$(function () {
    $('.delete-board-btn').click(function (event) {
        event.preventDefault();
        var board_id = $(this).attr('data-board-id');

        xtalert.alertConfirm({
            'msg': '您确定要删除本板块吗？',
            'confirmCallback': function () {
                // 把数据发送到后台
                xtajax.post({
                    'url': '/delete_board/',
                    'data': {
                        'board_id': board_id
                    },
                    'success': function (data) {
                        if(data['code'] == 200){
                            xtalert.alertSuccessToast('恭喜！板块删除成功！');
                            setTimeout(function(){
                                window.location.reload();
                            },800);
                        }else{
                            xtalert.alertInfoToast(data['message']);
                        }
                    }
                });
            }
        });
    });
});








