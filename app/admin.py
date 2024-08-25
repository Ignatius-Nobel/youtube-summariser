from django.contrib import admin
from .models import GeneratedContent, VideoDetail

class VideoDetailsInline(admin.StackedInline):
    model = VideoDetail
    extra = 0  # Number of extra blank forms to show

class GeneratedContentAdmin(admin.ModelAdmin):
    inlines = [VideoDetailsInline]

admin.site.register(GeneratedContent, GeneratedContentAdmin)


