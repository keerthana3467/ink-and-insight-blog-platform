from django.contrib import admin
from .models import Post, Category
@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ("title","author","category","status","published_at")
    list_filter = ("status","category")
    search_fields = ("title","content","author__username")
    prepopulated_fields = {"slug":("title",)}
admin.site.register(Category)
