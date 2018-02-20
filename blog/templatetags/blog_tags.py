from blog.models import Category, Comment, Post
from django import template
from django.db.models.aggregates import Count


register = template.Library()


@register.simple_tag
def get_categories():
    return Category.objects.annotate(num_posts=Count('post')).filter(num_posts__gt=0)


@register.simple_tag()
def get_reply_of(root_comment):
    reply_list = Comment.objects.filter(parent=root_comment)
    return reply_list


@register.inclusion_tag('blog/user_avatar.html')
def get_show_avatar(user):
    '''返回一个用户的展示头像<img>标签，优先用网络头像'''
    return {'user': user}


@register.simple_tag
def get_post_rank():
    return Post.objects.order_by('-views')[:10]


@register.simple_tag
def get_comment_rank():
    return Post.objects.annotate(num_comments=Count('comment')).order_by('-num_comments')[:10]