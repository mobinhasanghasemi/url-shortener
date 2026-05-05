from django.db import models
from django.db import transaction
from django.utils import timezone
from .models import ShortURL
from .utils import AdvancedCryptoEngine
from .cache_manager import CacheManager
import hashlib
import time
import threading

class URLShortenerService:
    def __init__(self):
        self.crypto = AdvancedCryptoEngine()
        self.cache = CacheManager()
        self._lock = threading.Lock()
    
    def shorten_url(self, long_url, ip=None, ua=None):
        normalized_url = ShortURL.normalize_url(long_url)
        url_hash = hashlib.sha256(normalized_url.encode()).hexdigest()
        cache_key = f'url_hash:{url_hash}'
        
        def fetch_from_db():
            with self._lock:
                obj, is_new = ShortURL.get_or_create_by_url(normalized_url, ip, ua)
                
                if is_new:
                    obj.save()
                    success = self._assign_short_code(obj)
                    if not success:
                        raise Exception('Failed to generate short code')
                
                return {
                    'short_code': obj.short_code,
                    'is_new': is_new,
                    'click_count': obj.click_count,
                    'long_url': obj.long_url
                }
        
        result = self.cache.get_or_set(cache_key, fetch_from_db, ttl=86400)
        
        if not result['is_new']:
            self._update_stats_async(result['short_code'])
        
        return result
    
    def _assign_short_code(self, obj):
        max_attempts = 10
        for attempt in range(max_attempts):
            try:
                short_code = self.crypto.generate_short_code(
                    obj.id, int(time.time() * 1000) + attempt
                )
                
                if not ShortURL.objects.filter(short_code=short_code).exists():
                    obj.short_code = short_code
                    obj.save(update_fields=['short_code'])
                    
                    self.cache.get_or_set(
                        f'code_to_url:{short_code}',
                        lambda: {'long_url': obj.long_url, 'id': obj.id},
                        ttl=86400
                    )
                    return True
            except Exception as e:
                print(f"Attempt {attempt + 1} failed: {e}")
                continue
        
        raise Exception('Failed to generate unique short code after max attempts')
    
    def get_long_url(self, short_code):
        cache_key = f'code_to_url:{short_code}'
        
        def fetch_from_db():
            obj = ShortURL.objects.filter(short_code=short_code, is_active=True).first()
            if obj:
                return {'long_url': obj.long_url, 'id': obj.id}
            return None
        
        result = self.cache.get_or_set(cache_key, fetch_from_db, ttl=3600)
        return result['long_url'] if result else None
    
    def _update_stats_async(self, short_code):
        def update():
            try:
                affected = ShortURL.objects.filter(short_code=short_code).update(
                    click_count=models.F('click_count') + 1,
                    last_accessed=timezone.now()
                )
                if affected > 0:
                    self.cache.invalidate(f'code_to_url:{short_code}')
            except Exception as e:
                print(f"Error updating stats: {e}")
        
        thread = threading.Thread(target=update)
        thread.daemon = True
        thread.start()