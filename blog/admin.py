from django.contrib import admin
from .models import BlogAuthor, BlogPost, Comments

# Register your models here.
@admin.register(BlogAuthor)
class BlogAuthorAdmin(admin.ModelAdmin):
    pass

class BlogCommentsInline(admin.TabularInline):
    model = Comments
    max_num = 0

@admin.register(BlogPost)
class BlogPostAdmin(admin.ModelAdmin):
    list_display = ('name', 'author', 'post_date')
    inlines = [BlogCommentsInline]

@admin.register(Comments)
class CommentsAdmin(admin.ModelAdmin):
    pass