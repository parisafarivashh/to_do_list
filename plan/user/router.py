from django.urls import path

from .consumer import UserConsumer


websocket_urls = [
    path('ws/user', UserConsumer.as_asgi())
]

