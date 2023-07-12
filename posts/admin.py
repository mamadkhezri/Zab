from django.contrib import admin
from .models import Post
# Register your models here.

@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
	prepopulated_fields = {'slug':('title',)}
	list_display = ('author', 'slug', 'created_date')


