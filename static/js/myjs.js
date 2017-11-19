// 评论回复系统
$(document).ready(function(){
        // 隐藏显示评论
        $('.hide-reply').click(function(){
            $(this).parent().next().slideToggle('fast',
                function(){
                    $(this).prev().children().text()=='收起回复' ? $(this).prev().children().text('回复') : $(this).prev().children().text('收起回复');
                    $(this).next().hide();
            });
        });
            // 添加评论
        $('.add-comment').click(function(){
            $(this).parent().parent().parent().next().show();
            $(this).parent().parent().parent().next().find('textarea').val('');
        });
            // 新增评论
        $('.comment').click(function(){
            $(this).parent().next().toggle();
        });
            // 回复评论
        $('.reply').click(function(){
            var toUser;
            toUser = $(this).parent().prev().text().split(':')[0];
            $(this).parent().parent().parent().next().show();
            $(this).parent().parent().parent().next().find('textarea').val('回复 '+ toUser + ' :');
        });
});
//返回顶部
//当滚动条的位置处于距顶部300像素以下时，跳转链接出现，否则消失
$(function () {
    $(window).scroll(function(){
        if ($(window).scrollTop()>300){
            $("#backtotop").show();
         }
        else
        {
            $("#backtotop").hide();
        }
    });
            //当点击跳转链接后，回到页面顶部位置
    $("#backtotop").click(function(){
        $('body,html').animate({scrollTop:0}, 500);
    });
});