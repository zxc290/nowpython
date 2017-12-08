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

    // 点击回复，改变reply_to的select选项中的值
    $('.reply').click(function(){
        var reply_to = $(this).attr('ID');
        $('#id_reply_to option:selected').val(reply_to);
        $('#cancel-reply').show();
    });

    // 取消回复
    $('#cancel-reply').click(function(){
        $('#id_reply_to option:selected').val('')
        $(this).hide();
    });
});