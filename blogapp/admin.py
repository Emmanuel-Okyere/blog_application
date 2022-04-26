from django.contrib import admin
from .models import Post
from .models import Comment
# Register your models here.
# admin.site.register(Post)
@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ("title","slug","author","publish","status")
    list_filter = ("status", "created", "publish","author")
    search_fields = ("title","body")
    raw_id_fields = ("author",)
    prepopulated_fields = {"slug": ("title",)}

@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ("name", "email","post","created","active")
    list_filter = ("active", "created","updated")
    search_fields = ("name","email", "body")
    