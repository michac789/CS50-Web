from django.contrib import admin
from .models import FollowPair, Post, Comment

# Register your models here.
admin.site.register(FollowPair)
admin.site.register(Post)
admin.site.register(Comment)
