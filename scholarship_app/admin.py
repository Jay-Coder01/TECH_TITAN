from django.contrib import admin
from .models import Scholarship, ForumTopic, ForumReply,Signup



@admin.register(Signup)
class SignupAdmin(admin.ModelAdmin):
    list_display = ('name', 'email')
    search_fields = ('name', 'email')
    # Ensure delete is enabled
    actions = ['delete_selected']

@admin.register(Scholarship)
class ScholarshipAdmin(admin.ModelAdmin):
    list_display = ('title', 'provider', 'amount', 'deadline', 'scholarship_type', 'education_level')
    list_filter = ('scholarship_type', 'education_level', 'deadline')
    search_fields = ('title', 'provider', 'description')
    date_hierarchy = 'deadline'

@admin.register(ForumTopic)
class ForumTopicAdmin(admin.ModelAdmin):
    list_display = ('title', 'user', 'created_at')
    list_filter = ('created_at',)
    search_fields = ('title', 'content')

@admin.register(ForumReply)
class ForumReplyAdmin(admin.ModelAdmin):
    list_display = ('topic', 'user', 'created_at')
    list_filter = ('created_at',)
    search_fields = ('content',)

admin.site.site_header = "Vidhyasathi Administration"
admin.site.site_title = "Vidhyasathi Admin Portal"
admin.site.index_title = "Welcome to Vidhyasathi Admin Portal"