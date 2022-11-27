from django.utils import timezone
from django.utils.deprecation import MiddlewareMixin


class LogTimeTakenMiddleware(MiddlewareMixin):

    def process_request(self, request):
        request.start_time = timezone.now()

    def process_response(self, request, response):
        total_time = timezone.now() - request.start_time
        request_method = request.META.get('REQUEST_METHOD')
        path_info = request.META.get('PATH_INFO')
        print('Time taken: {} Request method: {} url: {}'.format(
            total_time,
            request_method,
            path_info,
        ))
        return response
