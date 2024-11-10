"""
ASGI config for plan project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/4.0/howto/deployment/asgi/
"""

import os

import django
from django.core.asgi import get_asgi_application
from channels.routing import ProtocolTypeRouter
from channels.routing import URLRouter

from user.router import websocket_urls

from .middelware.custom_auth_middleware import CustomAuthMiddleware


os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'plan.settings')
django.setup()


application = ProtocolTypeRouter({
    "http": get_asgi_application(),
    "websocket": CustomAuthMiddleware(
        URLRouter(websocket_urls)
    )

})
