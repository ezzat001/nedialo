from django.utils.deprecation import MiddlewareMixin
from django.http import HttpResponseForbidden

class MediaAccessMiddleware(MiddlewareMixin):
    def process_request(self, request):
        if request.path.startswith('/media/'):
            return HttpResponseForbidden('Access denied to media files')
        return None