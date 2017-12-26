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
        $('#id_content').val('');
        var reply_to = $(this).attr('ID');
        $('#id_reply_to option:selected').val(reply_to);
        $('#button-id-cancel-reply').show();
        var reply_to_user = $('#c' + reply_to).text();
        $('.comment-form-title').children().html('回复:' + reply_to_user);
        $('html,body').animate({scrollTop:$('#comment-form').offset().top-150},1000);
    });

    // 评论提交后将页面刷新，并且定位到新的评论处
    if(sessionStorage.getItem('has_point')){
        var top = $(sessionStorage.getItem('new_point')).offset().top-100;
        $('body,html').animate({scrollTop:top}, 1000);
        window.location.hash = sessionStorage.getItem('new_point');
        sessionStorage.removeItem('has_point');
    };

    // 取消回复
    $('#button-id-cancel-reply').click(function(){
        $('#id_reply_to option:selected').val('')
        $('.comment-form-title').children().text('新评论');
        $(this).hide();
        $('#id_content').val('');
    });
    // ajax提交
    $('#comment-form').submit(function(e){

        if ($('.logout').length == 0){
            swal("请登录后再评论");
            return false;
        }
        if ($('#id_content').val() == 0){
                swal("评论内容不能为空！");
                return false;
            }
        e.preventDefault();
        $.ajaxSetup({
                data: {csrfmiddlewaretoken: '{{ csrf_token }}' }
            });

        $.ajax({
            type:$(this).attr('method'),
            url:$(this).attr('action'),
            data:$('#comment-form').serialize(),
            success:function(ret){
                // 清空内容
                $('#id_content').val('');
                sessionStorage.setItem('has_point', true);
                sessionStorage.setItem('new_point', ret.new_point);
                window.location.reload();
            },
            error:function(){
                alert(ret.msg);
            }
        });
    });
});

