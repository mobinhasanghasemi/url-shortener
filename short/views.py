from django.http import JsonResponse, HttpResponse
from django.views.decorators.http import require_POST, require_GET
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.gzip import gzip_page
from django.core.cache import cache
from django.shortcuts import redirect, render
from django_ratelimit.decorators import ratelimit
from .services import URLShortenerService
from .models import ShortURL
import logging

logger = logging.getLogger(__name__)
service = URLShortenerService()

def home(request):
    return render(request, 'short/home.html')

@gzip_page
@csrf_exempt
@require_POST
@ratelimit(key='ip', rate='100/m', method='POST')
def shorten_url(request):
    try:
        long_url = request.POST.get('long_url')
        
        if not long_url:
            return JsonResponse(
                {'error': 'لطفاً یک لینک وارد کنید'},
                status=400
            )
        
        ip = request.META.get('REMOTE_ADDR')
        ua = request.META.get('HTTP_USER_AGENT', '')[:500]
        
        result = service.shorten_url(long_url, ip, ua)
        
        return JsonResponse({
            'short_url': f'http://localhost:8000/{result["short_code"]}',
            'is_new': result['is_new'],
            'clicks': result['click_count']
        })
        
    except ValueError as e:
        return JsonResponse({'error': str(e)}, status=400)
    except Exception as e:
        logger.error(f"Error in shorten_url: {str(e)}")
        return JsonResponse({'error': 'خطای داخلی سرور'}, status=500)

@require_GET
def redirect_url(request, code):
    cache_key = f'redirect:{code}'
    long_url = cache.get(cache_key)
    
    if not long_url:
        long_url = service.get_long_url(code)
        
        if not long_url:
            return HttpResponse('URL not found', status=404)
        
        cache.set(cache_key, long_url, 3600)
    
    return redirect(long_url)

def stats(request, code):
    obj = ShortURL.objects.filter(short_code=code).first()
    if not obj:
        return JsonResponse({'error': 'URL not found'}, status=404)
    
    return JsonResponse({
        'short_code': obj.short_code,
        'long_url': obj.long_url,
        'click_count': obj.click_count,
        'created_at': obj.created_at,
        'is_active': obj.is_active
    })