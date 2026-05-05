import hashlib
import hmac
import secrets
import time
from django.conf import settings

class AdvancedCryptoEngine:
    def __init__(self):
        self.master_key = hashlib.pbkdf2_hmac(
            'sha256',
            settings.SECRET_KEY.encode(),
            b'url_shortener_super_salt_2025',
            100000
        )
    
    def generate_short_code(self, object_id, timestamp=None):
        if timestamp is None:
            timestamp = int(time.time() * 1000)
        
        data = f'{object_id}:{timestamp}'.encode()
        
        hmac_hash = hmac.new(
            self.master_key,
            data,
            hashlib.sha256
        ).digest()
        
        return self._base62_encode(hmac_hash[:8])
    
    def _base62_encode(self, data):
        chars = 'abcdefghijkmnopqrstuvwxyzABCDEFGHJKLMNPQRSTUVWXYZ123456789'
        num = int.from_bytes(data, 'big')
        
        if num == 0:
            return chars[0]
        
        result = []
        while num > 0:
            num, rem = divmod(num, 62)
            result.append(chars[rem])
        
        result = ''.join(reversed(result))
        
        while len(result) < 6:
            result = 'a' + result
        
        return result[:8]