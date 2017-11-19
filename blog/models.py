# -*- coding:utf-8 -*-
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.validators import MaxValueValidator
from django.shortcuts import reverse
import requests


# Create your models here.
class User(AbstractUser):
    email = models.EmailField(verbose_name='电子邮箱地址', unique=True)
    nickname = models.CharField(max_length=30, verbose_name='昵称')
    age = models.IntegerField(blank=True, null=True, verbose_name='年龄', validators=[MaxValueValidator(150)])
    intro = models.TextField(max_length=100, blank=True, null=True, verbose_name='个人简介')
    mobile = models.CharField(max_length=11, blank=True, null=True, unique=True, verbose_name='手机')

    class Meta:
        verbose_name = '用户'
        verbose_name_plural = verbose_name
        ordering = ['-id']

    def __str__(self):
        return self.username


class Category(models.Model):
    name = models.CharField(max_length=20, verbose_name='分类名')

    class Meta:
        verbose_name = '分类'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('category', kwargs={'cate_name': self.name})


class Post(models.Model):
    title = models.CharField(max_length=80, verbose_name='标题')
    intro = models.TextField(max_length=300, verbose_name='描述', blank=True)
    content = models.TextField(verbose_name='正文')
    pub_time = models.DateTimeField(auto_now_add=True, verbose_name='发布时间')
    author = models.ForeignKey(User, verbose_name='作者')
    category = models.ManyToManyField(Category, verbose_name='分类', blank=True)

    class Meta:
        verbose_name = '文章'
        verbose_name_plural = verbose_name
        ordering = ['-pub_time']

    def get_absolute_url(self):
        return reverse('post_detail', kwargs={'pk': self.pk})

    def __str__(self):
        return self.title


class Comment(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField(max_length=255)
    text = models.TextField()
    created_time = models.DateTimeField(auto_now_add=True)
    floor = models.CharField(max_length=100, blank=True)
    post = models.ForeignKey(Post)

    class Meta:
        verbose_name = '评论'
        verbose_name_plural = verbose_name
        ordering = ['created_time']

    def __str__(self):
        return self.text[:30]


class Reply(models.Model):
    comment = models.ForeignKey(Comment, verbose_name='评论')
    name = models.CharField(max_length=100)
    text = models.TextField()
    created_time = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = '回复'
        verbose_name_plural = verbose_name
        ordering = ['created_time']

    def __str__(self):
        return self.text[:30]