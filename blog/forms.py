from .models import User, Comment
from django.forms import ModelForm
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Field, Button, Submit


class CommentForm(ModelForm):

    def __init__(self, *args, **kwargs):
        super(CommentForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper(self)
        self.helper.form_show_labels = False
        self.helper.form_id = 'comment-form'
        self.helper.form_method = 'post'
        self.helper.form_action = 'ajax_comment'
        self.helper.layout = Layout(
            Field('content', rows=6, placeholder='请输入评论内容'),
            Field('parent', ),
            Field('reply_to',),
            Field('post',),
            Submit('confirm-reply', '提交评论', css_class='pull-right'),
            Button('cancel-reply', '取消回复', css_class='btn-danger pull-right')
        )

    class Meta:
        model = Comment
        fields = ('content', 'parent', 'reply_to', 'post')


class UserDetailForm(ModelForm):

    class Meta:
        model = User
        fields = ('nickname', 'avatar')
