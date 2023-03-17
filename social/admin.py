from django.contrib import admin
from social.models import UserProfile,Following,Post,Comment,Like

# Register your models here.
admin.site.register(UserProfile)
admin.site.register(Following)
admin.site.register(Post)
admin.site.register(Comment)
admin.site.register(Like)