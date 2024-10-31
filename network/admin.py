from django.contrib import admin

# Register your models here.

from .models import *

class PostAdmin(admin.ModelAdmin):
    readonly_fields = ('post_nb', 'id',)  # Make post_nb read-only
    list_display = ('id', 'creator', 'post_nb', 'message', 'timestamp')

admin.site.register(User)
admin.site.register(Post, PostAdmin)
admin.site.register(Tag)
admin.site.register(Profile)
admin.site.register(Comment)
admin.site.register(Reaction)
admin.site.register(PostImages)

