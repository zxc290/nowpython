from .models import User, Comment
from django.forms import ModelForm
from django import forms
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Field, Button, Submit

'''auth自带signup,暂时取代register
class RegisterForm(ModelForm):
    password = forms.CharField(label='输入密码', widget=forms.PasswordInput)
    password2 = forms.CharField(label='确认密码', widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ('username', 'email')

    def clean_password2(self):
        cd = self.cleaned_data
        if cd['password'] != cd['password2']:
            raise forms.ValidationError('输入的密码不一致')
        return cd['password2']

    def clean_email(self):
        cd = self.cleaned_data
        if User.objects.filter(email=cd['email']).count() > 0:
            raise forms.ValidationError('该邮箱已注册')
        return cd['email']
'''

class CommentForm(ModelForm):

    def __init__(self, *args, **kwargs):
        super(CommentForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper(self)
        self.helper.form_show_labels = False
        self.helper.form_id = 'comment-form'
        self.helper.form_method = 'post'
        self.helper.form_action = 'ajax_comment'
        self.helper.layout = Layout(
            Field('content',),
            Field('parent',),
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
