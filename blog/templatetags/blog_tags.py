from blog.models import Category, Comment
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

