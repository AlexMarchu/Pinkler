from django.contrib import admin
from .models import Post, Comment, Like

class PostAdmin(admin.ModelAdmin):
    list_display = ('content', 'author', 'created', 'number_of_likes')
    search_fields = ('content',)

    def number_of_likes(self, obj):
        return obj.liked.count()

    number_of_likes.short_description = 'Количество лайков'

class LikeAdmin(admin.ModelAdmin):
    list_display = ('user', 'post', 'value', 'created')
    list_filter = ('post',)

admin.site.register(Post, PostAdmin)
admin.site.register(Comment)
admin.site.register(Like, LikeAdmin)