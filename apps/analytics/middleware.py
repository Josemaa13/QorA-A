import re
import logging
from .services.services import track_page_view

logger = logging.getLogger(__name__)

class AnalyticsMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
        self.track_paths = [
            r'^/$',                     # Home
            r'^/publications/.*',       # Publications
            r'^/users/.*',              # User profiles
            r'^/recommendations/.*',    # Recommendations
            r'^/@.*',                   # User profiles with @
        ]

    def __call__(self, request):
        response = self.get_response(request)
        
        if request.method == 'GET' and response.status_code == 200:
            path = request.path
            if any(re.match(pattern, path) for pattern in self.track_paths):
                user_id = request.user.id if request.user.is_authenticated else None
                ip_address = self.get_client_ip(request)
                try:
                    track_page_view(user_id, path, ip_address)
                except Exception as e:
                    logger.error(f"Failed to track page view: {e}")
                    
        return response

    def get_client_ip(self, request):
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            ip = x_forwarded_for.split(',')[0]
        else:
            ip = request.META.get('REMOTE_ADDR')
        return ip
