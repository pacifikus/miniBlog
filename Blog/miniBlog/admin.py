from django.contrib import admin
from .models import Blogger, Blog, BlogMessage, Comment


class BlogInline(admin.StackedInline):
    model = Blog
    extra = 1


class BlogMessageInline(admin.StackedInline):
    model = BlogMessage
    extra = 1


@admin.register(Blogger)
class BloggerAdmin(admin.ModelAdmin):
    inlines = [BlogInline]
    list_display = ('get_username', 'name')

    def get_username(self, obj):
        return obj.user.username

    get_username.admin_order_name = 'user__username'
    get_username.short_description = 'Имя пользователя'


@admin.register(Blog)
class BlogAdmin(admin.ModelAdmin):
    inlines = [BlogMessageInline]
    list_display = ('blog_name', 'get_blogger')

    def get_blogger(self, obj):
        return obj.blogger.user.username
    get_blogger.admin_order_name = 'blogger__user__username'
    get_blogger.short_description = 'Автор'


@admin.register(BlogMessage)
class BlogMessageAdmin(admin.ModelAdmin):
    list_display = ('title', 'get_blog')
    list_filter = ['create_date']

    def get_blog(self, obj):
        return obj.blog.blog_name
    get_blog.admin_order_name = 'blog__blog_name'
    get_blog.short_description = 'Блог'


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('get_author', 'get_short_text', 'create_date')
    list_filter = ['create_date']

    def get_author(self, obj):
        return obj.author.username

    get_author.admin_order_name = 'author__username'
    get_author.short_description = 'Автор'


