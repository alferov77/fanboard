from django.contrib import admin
from .models import CustomUser, Newsletter

@admin.register(CustomUser)
class CustomUserAdmin(admin.ModelAdmin):
    list_display = ('username', 'email', 'is_staff', 'is_active')
    search_fields = ('username', 'email')

@admin.register(Newsletter)
class NewsletterAdmin(admin.ModelAdmin):
    list_display = ('subject', 'created_at')
    search_fields = ('subject', 'message')
    ordering = ('-created_at',)