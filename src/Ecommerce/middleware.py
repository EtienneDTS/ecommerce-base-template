from django.contrib.sessions.models import Session
from django.utils import timezone
from shop.models import CartProduct, Cart
from accounts.models import CustomUser
from django.utils.cache import add_never_cache_headers

class CustomSessionCleanupMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        sessions = Session.objects.all()
        expired_sessions = [session for session in sessions if session.expire_date <= timezone.now()]
        expired_session_keys = [s.session_key for s in expired_sessions]
        for expired_session_key in expired_session_keys:
            Cart.objects.filter(session_key=expired_session_key).delete()
            Session.objects.filter(session_key=expired_session_key).delete()
        response = self.get_response(request)
        return response
    
class DisableCacheMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)
        add_never_cache_headers(response)
        return response