from django.contrib import admin
from .models import User, Post, Category, Comment
# Register your models here.


class UserAdmin(admin.ModelAdmin):
    list_display = ('username', 'email')


class PostAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'pub_time')
    list_filter = ('author', 'pub_time')
    # 分类多对多关系
    filter_horizontal = ('category',)
    raw_id_fields = ('author',)


class CategoryAdmin(admin.ModelAdmin):
    pass


class ReplyAdmin(admin.ModelAdmin):
    list_display = ('name', 'text')


class CommentAdmin(admin.ModelAdmin):
    pass


admin.site.register(User, UserAdmin)
admin.site.register(Post, PostAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(Comment, CommentAdmin)