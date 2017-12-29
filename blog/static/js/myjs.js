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
    $('.comment-list').delegate('.reply', 'click', function(){
        $('#id_content').val('');
        var reply_to = $(this).attr('ID');
        $('#id_reply_to option:selected').val(reply_to);
        $('#button-id-cancel-reply').show();
        var reply_to_user = $('#c' + reply_to).text();
        $('.comment-form-title').children().html('回复:' + reply_to_user);
        $('html,body').animate({scrollTop:$('#comment-form').offset().top-150}, 500);
    });


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

        e.preventDefault();
        $.ajaxSetup({
                data: {csrfmiddlewaretoken: '{{ csrf_token }}' }
            });

        $.ajax({
            type:$(this).attr('method'),
            url:$(this).attr('action'),
            data:$('#comment-form').serialize(),
            success:function(ret){
                $('#id_content').val('');
                $('.comment-list').prepend(ret);
                var count = Number($('#comment-count').text()) + 1;
                $('#comment-count').text(count);
                if ($('.no-comment').length >0 ){
                    $('.no-comment').remove();
                }
                $('html,body').animate({scrollTop:$('.comment-list').offset().top-150}, 500);
            },
            error:function(){
                alert(ret.msg);
            }
        });
    });

    // 滚动加载
    var page = 1;
    var empty_page = false;
    var block_request = false;

    $(window).scroll(function() {
        var margin = $(document).height() - $(window).height() - 200;
        if  ($(window).scrollTop() > margin && empty_page == false && block_request == false) {
            block_request = true;
            page += 1;
            $.get('?page=' + page, function(data) {
                if(data == '')
                {
                    empty_page = true;
                }
                else {
                    block_request = false;
                    $('.comment-list').append(data);
                }
            });
        }
    });
});

