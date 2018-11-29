from django.contrib import admin
from .models import Post

class PostModelAdmin(admin.ModelAdmin):
    list_display = ["title", "timestamp", "updated"]
    list_display_links = ["timestamp", "updated", "title"]
    list_filter = ["updated"]
    search_fields = ["title", "content"]
    class Meta:
        model = Post
# Register your models here.
admin.site.register(Post, PostModelAdmin)

