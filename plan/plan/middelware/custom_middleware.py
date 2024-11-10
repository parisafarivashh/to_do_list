import ujson
from django.utils import timezone
from django.utils.deprecation import MiddlewareMixin
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync
from rest_framework.response import Response


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


class SendResponseDataToWebsocket(MiddlewareMixin):

    def process_response(self, request, response):
        if not isinstance(response, Response):
            return response

        path = request.path.replace('/api/', '')
        path = f"{request.method.lower()}_{path}".replace('/', '_')

        channel_layer = get_channel_layer()
        async_to_sync(channel_layer.group_send)(
            f'user_{request.user.id}',
            {
                'type': 'send_data',
                'data': ujson.dumps({path: response.data}),
            }
        )
        return response
