from django.contrib import admin
from .models import User, Post, Category, Comment, Reply
# Register your models here.


class UserAdmin(admin.ModelAdmin):
    list_display = ('username', 'email', 'age', 'intro')


class PostAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'pub_time')
    list_filter = ('author', 'pub_time')
    # 分类多对多关系
    filter_horizontal = ('category',)
    raw_id_fields = ('author',)


class CategoryAdmin(admin.ModelAdmin):
    pass


class CommentAdmin(admin.ModelAdmin):
    list_display = ('name', 'text')


class ReplyAdmin(admin.ModelAdmin):
    list_display = ('name', 'text')


admin.site.register(User, UserAdmin)
admin.site.register(Post, PostAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(Comment, CommentAdmin)
admin.site.register(Reply, ReplyAdmin)