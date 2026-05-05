from django.contrib import admin
from .models import ShortURL

@admin.register(ShortURL)
class ShortURLAdmin(admin.ModelAdmin):
    list_display = ['short_code', 'long_url', 'click_count', 'created_at', 'is_active', 'ip_address']
    list_filter = ['is_active', 'created_at']
    search_fields = ['short_code', 'long_url', 'ip_address']
    readonly_fields = ['url_hash', 'click_count', 'ip_address', 'user_agent']
    list_editable = ['is_active']
    list_per_page = 50