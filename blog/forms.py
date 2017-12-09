from .models import User, Comment
from django.forms import ModelForm
from django import forms


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


class CommentForm(ModelForm):

    class Meta:
        model = Comment
        fields = ('content', 'parent', 'reply_to', 'post')


class UserDetailForm(ModelForm):
    class Meta:
        model = User
        fields = ('nickname', 'avatar')
