/**
 * Created by Administrator on 2017/5/23 0023.
 */
//初始化编辑器
$(function(){
   var editor =new wangEditor('editor');
    editor.create();
    window.editor = editor;
});
//初始化七牛
$(function () {
   var progressBox = $('#progress-box');
    var progressBar = progressBox.children(0);
    var upload = $('#upload-btn');
   xtqiniu.setUp({
       'browse_btn': 'upload-btn',
       'success': function (up,file,info) {
           var fileUrl = file.name;
           if(file.type.indexOf('video') >= 0){
               // 视频
               var videoTag = "<video width='640' height='480' controls><source src="+fileUrl+"></video>";
               window.editor.$txt.append(videoTag);
           }else{
               var imgTag = "<img src="+fileUrl+">"
               window.editor.$txt.append(imgTag);
           }
       },
       'fileadded':function(){
           progressBox.show();
           upload.button('loading');
       },
       'progress':function(up,file){
           var percent = file.percent;
           progressBar.attr('aria-valuenow',percent);
           progressBar.css('width',percent+'%');
           progressBar.text(percent+'%');
       },
       'complete':function(){
           progressBox.hide();
           progressBar.attr('aria-valuenow',0);
           progressBar.css('width','0%');
           progressBar.text('0%');
           upload.button('reset');
       }
   });
});