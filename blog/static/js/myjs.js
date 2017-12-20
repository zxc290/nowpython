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
        e.preventDefault();
        $.ajax({
            type:$(this).attr('method'),
            url:$(this).attr('action'),
            data:$('#comment-form').serialize(),
            dataType:'json',
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
/* 拼接
                var parent_id = ret['parent_id'];
                var avatar_url = ret['avatar_url'];
                var id = ret['id'];
                var author = ret['author'];
                var created = ret['created'];
                var content = ret['content'];
                if (parent_id == null)
                {
                    //根评论
                    var div1 = $("<div class='root-comment'></div>");

                    var div2 = $("<div class='col-sm-1 comment-avatar'></div>");
                    var img = $("<img class='img-rounded' src=" + avatar_url +  "/>");

                    div2.append(img);

                    div3 = $("<div class='col-sm-11'></div>");
                    span1 = $("<span></span>");
                    span1.attr('id', 'c' + id);
                    span1.append(author);
                    div3.append(span1);

                    span2 = $("<span class='pull-right'></span>");
                    span2.append(created);
                    div3.append(span2);

                    div4 = $("<div class='comment-content'></div>");
                    div4.append(content);
                    div3.append(div4);

                    span3 = $("<span></span>");
                    a1 = $("<a href='#comment-form' class='reply pull-right'>回复</a>");
                    a1.attr('id', id);
                    span3.append(a1);
                    div3.append(span3);

                    div1.append(div2);
                    div1.append(div3);

                    $('.comment-list').append(div1);
                    if ($('.no-comment').length > 0)
                    {
                        $('.no-comment').remove();
                    }
                    // 定位到新评论
                }
                else
                {
                    //子评论
                    var div1 = $("<div class='child-comment'></div>");

                    var div2 = $("<div class='col-sm-1 comment-avatar'></div>");
                    var img = $("<img class='img-rounded' src=" + avatar_url +  "/>");

                    div2.append(img);

                    div3 = $("<div class='col-sm-11'></div>");
                    span1 = $("<span></span>");
                    span1.attr('id', 'c' + id);
                    span1.append(author);
                    span2 = $("<span class='glyphicon glyphicon-share-alt'></span>");
                    span3 = $("<span></span>");
                    parent_author = $('#c' + parent_id).text();
                    span3.append(parent_author);
                    span4 = span1 + '&nbsp;' + span2 + '&nbsp;' + span3;
                    div3.append(span4);

                    span5 = $("<span class='pull-right'></span>");
                    span5.append(created);
                    div3.append(span5);

                    div4 = $("<div class='comment-content'></div>");
                    div4.append(content);
                    div3.append(div4);

                    span6 = $("<span></span>");
                    a1 = $("<a href='#comment-form' class='reply pull-right'>回复</a>");
                    a1.attr('id', id);
                    span6.append(a1);
                    div3.append(span6);

                    div1.append(div2);
                    div1.append(div3);

                    $('#' + parent_id).parents('.root-comment').next().append(div1);

                }
*/
