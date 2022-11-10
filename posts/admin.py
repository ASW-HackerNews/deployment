from django.contrib import admin
from .models import Post, Like, Comment, Ask, Link
# Register your models here.
admin.site.register(Post)
admin.site.register(Like)
admin.site.register(Comment)
admin.site.register(Ask)
admin.site.register(Link)