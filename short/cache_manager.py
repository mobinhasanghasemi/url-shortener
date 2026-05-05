from django.core.cache import cache
from django.core.cache.utils import make_template_fragment_key
import pickle
import zlib
import threading
from concurrent.futures import ThreadPoolExecutor
import time

class CacheManager:
    def __init__(self):
        self.executor = ThreadPoolExecutor(max_workers=20)
        self.local_cache = {}
        self.local_cache_time = {}
        self.lock = threading.Lock()
    
    def get_or_set(self, key, callback, ttl=3600):
        with self.lock:
            if key in self.local_cache and time.time() - self.local_cache_time.get(key, 0) < 60:
                return self.local_cache[key]
        
        cached = cache.get(key)
        if cached is not None:
            try:
                data = pickle.loads(zlib.decompress(cached))
                with self.lock:
                    self.local_cache[key] = data
                    self.local_cache_time[key] = time.time()
                return data
            except:
                pass
        
        data = callback()
        
        try:
            compressed = zlib.compress(pickle.dumps(data), level=6)
            cache.set(key, compressed, ttl)
            with self.lock:
                self.local_cache[key] = data
                self.local_cache_time[key] = time.time()
        except:
            pass
        
        return data
    
    def set_many(self, data_dict, ttl=3600):
        cache_data = {}
        for key, value in data_dict.items():
            try:
                compressed = zlib.compress(pickle.dumps(value), level=6)
                cache_data[key] = compressed
            except:
                cache_data[key] = value
        
        cache.set_many(cache_data, ttl)
    
    def invalidate(self, key):
        cache.delete(key)
        with self.lock:
            if key in self.local_cache:
                del self.local_cache[key]
            if key in self.local_cache_time:
                del self.local_cache_time[key]
    
    def invalidate_pattern(self, pattern):
        with self.lock:
            keys_to_delete = [k for k in self.local_cache.keys() if pattern in k]
            for key in keys_to_delete:
                del self.local_cache[key]
                del self.local_cache_time[key]
        cache.delete_pattern(pattern)
    
    def clear_all(self):
        cache.clear()
        with self.lock:
            self.local_cache.clear()
            self.local_cache_time.clear()