from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from .models import User, Post, Comment, Reply
from django.forms import ModelForm, TextInput
from django import forms


class CommentForm(ModelForm):
    class Meta:
        model = Comment
        fields = ['text']


class ReplyForm(ModelForm):
    class Meta:
        model = Reply
        fields = ['text']

class LoginForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)


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


class EditProfileForm(ModelForm):

    class Meta:
        model = User
        fields = ('nickname', 'age', 'intro', 'mobile')


class PostForm(ModelForm):

    class Meta:
        model = Post
        exclude = ['draft', 'review', 'author']














'''
class LoginForm(forms.Form):
    username = forms.CharField(label='用户名', max_length=20,
                               widget=forms.TextInput(
                                   attrs={
                                       'class': 'form-control',
                                       'placeholder': '用户名'
                                   }
                               ))

    password = forms.CharField(label='密码', max_length=20,
                               widget=forms.PasswordInput(
                                   attrs={
                                       'class': 'form-control',
                                       'placeholder': '密码'
                                   }
                               ))



    def clean(self):
        cleaned_data = super(LoginForm, self).clean()
        username = cleaned_data.get('username')

        if not User.objects.filter(username=username).exists():
            raise forms.ValidationError('该用户不存在')

        return self.cleaned_data


class RegisterForm(forms.Form):
    username = forms.CharField(label='用户名', max_length=20,
                               widget=forms.TextInput(
                                   attrs={
                                       'class': 'form-control',
                                       'placeholder': '用户名'
                                   }
                               ))

    email = forms.EmailField(label='电子邮箱', max_length=20,
                             widget=forms.EmailInput(
                                 attrs={
                                     'class': 'form-control',
                                     'placeholder': '电子邮箱'
                                 }
                             ))

    password = forms.CharField(label='密码', max_length=20,
                               widget=forms.PasswordInput(
                                   attrs={
                                       'class': 'form-control',
                                       'placeholder': '密码'
                                   }
                               ))

    password2 = forms.CharField(label='确认密码', max_length=20,
                                widget=forms.PasswordInput(
                                    attrs={
                                        'class': 'form-control',
                                        'placeholder': '确认密码'
                                    }
                                ))

    def clean(self):
        cleaned_data = super(RegisterForm, self).clean()
        username = cleaned_data.get('username')
        email = cleaned_data.get('email')
        password = cleaned_data.get('password')
        password2 = cleaned_data.get('password2')

        if User.objects.filter(username=username).exists():
            raise forms.ValidationError('用户名已存在')

        if User.objects.filter(email=email).exists():
            raise forms.ValidationError('邮箱已存在')

        if password != password2:
            raise forms.ValidationError('密码不一致')

        return self.cleaned_data
'''