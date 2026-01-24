from django.contrib import admin
from .models import ProjectInquiry


@admin.register(ProjectInquiry)
class ProjectInquiryAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'ip_address', 'created_at')
    search_fields = ('name', 'email', 'message')
