from django.contrib import admin
from blog.models import Post

# Register your models here.
class PostAdmin(admin.ModelAdmin):
    raw_id_fields = ['user']
    fields = ['user', 'title', 'content']
    list_display = ['user', 'title', 'created']
    list_filter = ['user', 'created']


admin.site.register(Post, PostAdmin)