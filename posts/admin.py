from django.contrib import admin
from .models import Post, Comment, vote, Image, Video, Audio
# Register your models here.

@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
	prepopulated_fields = {'slug':('title',)}
	list_display = ('author', 'slug', 'created_date')



@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
	list_display = ('author', 'post', 'created', 'is_reply')
	raw_id_fields = ('author', 'post', 'reply')

admin.site.register(vote)
admin.site.register(Image)
admin.site.register(Audio)
admin.site.register(Video)


