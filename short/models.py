from django.db import models
from django.core.validators import URLValidator
from django.core.exceptions import ValidationError
from django.utils import timezone
from cryptography.fernet import Fernet
from django.conf import settings
import hashlib
import re
import secrets
import base64

class ShortURL(models.Model):
    long_url = models.TextField()
    url_hash = models.CharField(max_length=64, unique=True, db_index=True, default='', blank=True)
    short_code = models.CharField(max_length=20, unique=True, db_index=True)
    created_at = models.DateTimeField(auto_now_add=True)
    click_count = models.PositiveIntegerField(default=0)
    last_accessed = models.DateTimeField(null=True, blank=True)
    is_active = models.BooleanField(default=True)
    encrypted_data = models.TextField(null=True, blank=True)
    access_token = models.CharField(max_length=255, null=True, blank=True)
    ip_address = models.GenericIPAddressField(null=True, blank=True)
    user_agent = models.TextField(null=True, blank=True)
    
    class Meta:
        indexes = [
            models.Index(fields=['url_hash']),
            models.Index(fields=['short_code']),
            models.Index(fields=['-click_count']),
            models.Index(fields=['created_at']),
            models.Index(fields=['is_active']),
        ]
    
    @classmethod
    def normalize_url(cls, url):
        url = url.strip()
        if not url.startswith(('http://', 'https://')):
            url = 'https://' + url
        url = re.sub(r'/+$', '', url)
        url = re.sub(r'/$', '', url)
        return url
    
    @classmethod
    def get_or_create_by_url(cls, long_url, ip=None, ua=None):
        long_url = cls.normalize_url(long_url)
        validator = URLValidator()
        try:
            validator(long_url)
        except ValidationError:
            raise ValueError('Invalid URL format')
        
        url_hash = hashlib.sha256(long_url.encode()).hexdigest()
        existing = cls.objects.filter(url_hash=url_hash, is_active=True).first()
        if existing:
            return existing, False
        
        obj = cls(
            long_url=long_url, 
            url_hash=url_hash,
            ip_address=ip,
            user_agent=ua
        )
        return obj, True
    
    def increment_click(self):
        self.click_count = models.F('click_count') + 1
        self.last_accessed = timezone.now()
        self.save(update_fields=['click_count', 'last_accessed'])