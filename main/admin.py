from django.contrib import admin
from .models import ProjectInquiry, Review, Project, ProjectImage


@admin.register(ProjectInquiry)
class ProjectInquiryAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'phone', 'ip_address', 'created_at')
    search_fields = ('name', 'email', 'message')


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ('name', 'service_type', 'rating', 'is_approved', 'created_at')
    list_filter = ('is_approved', 'service_type', 'rating')
    search_fields = ('name', 'comment')
    actions = ['approve_reviews']

    def approve_reviews(self, request, queryset):
        queryset.update(is_approved=True)
    approve_reviews.short_description = "Approve selected reviews"


class ProjectImageInline(admin.TabularInline):
    model = ProjectImage
    extra = 1


@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ('title', 'client_name', 'service_type', 'is_published', 'completion_date', 'created_at')
    list_filter = ('is_published', 'service_type', 'completion_date')
    search_fields = ('title', 'client_name', 'description')
    inlines = [ProjectImageInline]
    fieldsets = (
        (None, {
            'fields': ('title', 'slug', 'client_name', 'description', 'service_type', 'main_image', 'completion_date', 'is_published')
        }),
    )
