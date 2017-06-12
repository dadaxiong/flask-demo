/**
 * Created by Administrator on 2017/5/4 0004.
 */
$(function () {
    var btn = $('#graph-captcha-btn');
    btn.css('cursor','pointer');
    btn.click(function (event) {
        event.preventDefault();
        var imgTag = $(this).children('img');
        var oldSrc = imgTag.attr('src');
        var href = xtparam.setParam(oldSrc,'xx',Math.random());
        imgTag.attr('src',href);
    });
});