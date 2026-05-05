from django.core.exceptions import PermissionDenied
from django.utils.deprecation import MiddlewareMixin
import re
import time
from collections import defaultdict
import threading

class SecurityMiddleware(MiddlewareMixin):
    sync_capable = True
    async_capable = False
    
    def __init__(self, get_response):
        super().__init__(get_response)
        self.get_response = get_response
        self.request_counts = defaultdict(list)
        self.blocked_ips = set()
        self.lock = threading.Lock()
    
    def __call__(self, request):
        if request.method == 'POST' and '/api/' in request.path:
            return self.get_response(request)
        
        client_ip = self._get_client_ip(request)
        
        if client_ip in self.blocked_ips:
            raise PermissionDenied('IP is blocked')
        
        if self._is_rate_limited(client_ip):
            with self.lock:
                self.blocked_ips.add(client_ip)
            raise PermissionDenied('Rate limit exceeded')
        
        if self._has_malicious_content(request):
            raise PermissionDenied('Malicious request detected')
        
        if request.method == 'GET' and self._is_sql_injection(request):
            raise PermissionDenied('SQL injection detected')
        
        request.client_ip = client_ip
        
        response = self.get_response(request)
        
        response['X-Frame-Options'] = 'DENY'
        response['X-Content-Type-Options'] = 'nosniff'
        response['X-XSS-Protection'] = '1; mode=block'
        response['Referrer-Policy'] = 'strict-origin-when-cross-origin'
        
        if hasattr(request, 'client_ip'):
            response['X-Client-IP'] = request.client_ip
        
        return response
    
    def _get_client_ip(self, request):
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            return x_forwarded_for.split(',')[0].strip()
        return request.META.get('REMOTE_ADDR', '127.0.0.1')
    
    def _is_rate_limited(self, ip):
        if ip == '127.0.0.1':
            return False
            
        now = time.time()
        with self.lock:
            self.request_counts[ip] = [t for t in self.request_counts[ip] if now - t < 60]
            
            if len(self.request_counts[ip]) > 100:
                return True
            
            self.request_counts[ip].append(now)
            return False
    
    def _has_malicious_content(self, request):
        dangerous = ['<script', 'javascript:', 'vbscript:', 'onload=', 'onerror=']
        
        data = str(request.GET.dict())
        data_lower = data.lower()
        
        for pattern in dangerous:
            if pattern in data_lower:
                return True
        return False
    
    def _is_sql_injection(self, request):
        sql_patterns = [
            r"(\%27)|(\')|(\-\-)|(\%23)|(#)",
            r"union.*select",
            r"select.*from",
            r"insert.*into",
            r"delete.*from",
            r"drop.*table",
        ]
        
        data = str(request.GET.dict())
        data_lower = data.lower()
        
        for pattern in sql_patterns:
            if re.search(pattern, data_lower, re.IGNORECASE):
                return True
        return False