# -*- coding:utf-8 -*-
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.shortcuts import reverse
from imagekit.models import ProcessedImageField
from imagekit.processors import ResizeToFill


# Create your models here.
class User(AbstractUser):
    nickname = models.CharField(verbose_name='昵称', max_length=50)
    avatar = ProcessedImageField(upload_to='avatar', default='avatar/default.png', verbose_name='头像',
                                 # 处理为48*48尺寸
                                 processors=[ResizeToFill(48, 48)],
                                 )


    class Meta:
        verbose_name = '用户'
        verbose_name_plural = verbose_name
        ordering = ['-id']

    def __str__(self):
        return self.username

    def save(self, *args, **kwargs):
        if len(self.avatar.name.split('/')) == 1:
            self.avatar.name = self.username + '/' + self.avatar.name
        # 昵称默认为用户名
        if not self.nickname:
            self.nickname = self.username
        super(User, self).save()


class Category(models.Model):
    name = models.CharField(max_length=20, verbose_name='分类名', unique=True)

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
    cover = ProcessedImageField(upload_to='cover', default='cover/default_cover.jpg', verbose_name='封面',
                                processors=[ResizeToFill(200, 112)],
                                )
    content = models.TextField(verbose_name='正文')
    pub_time = models.DateTimeField(auto_now_add=True, verbose_name='发布时间')
    author = models.ForeignKey(User, verbose_name='作者')
    category = models.ManyToManyField(Category, verbose_name='分类', blank=True)
    views = models.PositiveIntegerField(default=0, verbose_name='阅读数')

    class Meta:
        verbose_name = '文章'
        verbose_name_plural = verbose_name
        ordering = ['-pub_time']

    def get_absolute_url(self):
        return reverse('post_detail', kwargs={'pk': self.pk})

    def get_pre(self):
        return Post.objects.filter(pk__lt=self.pk).order_by('-pk').first()

    def get_next(self):
        return Post.objects.filter(pk__gt=self.pk).order_by('pk').first()

    def increase_views(self):
        self.views += 1
        self.save(update_fields=['views'])

    def __str__(self):
        return self.title


class Comment(models.Model):
    content = models.TextField(verbose_name='评论内容')
    created = models.DateTimeField(auto_now_add=True, verbose_name='评论时间')
    author = models.ForeignKey(User, verbose_name='评论人')
    post = models.ForeignKey(Post, verbose_name='所属文章')
    parent = models.ForeignKey('self', verbose_name='根评论', blank=True, null=True, related_name='child_comment')
    reply_to = models.ForeignKey('self', verbose_name='父级评论', blank=True, null=True, related_name='direct_child')
    page = models.CharField(max_length=10, verbose_name='所在页', blank=True, null=True)

    class Meta:
        verbose_name = '评论'
        verbose_name_plural = verbose_name
        ordering = ['created']

    def __str__(self):
        return self.content[:20]

    def save(self, *args, **kwargs):
        if self.parent:
            self.page = self.parent.page
        else:
            objects = self.post.comment_set.all().filter(parent=None)
            self.page = objects.count() // 10 + 1
        super(Comment, self).save()