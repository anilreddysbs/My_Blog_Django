from django.contrib import admin

# Register your models here.
from .models import Post, Comment,Profile,ContactMessage

admin.site.register(Post)
admin.site.register(Comment)
admin.site.register(Profile)
admin.site.register(ContactMessage)

