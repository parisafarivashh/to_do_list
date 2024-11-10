from channels.auth import AuthMiddleware
from channels.db import database_sync_to_async
from django.contrib.auth.models import AnonymousUser

from user.models import Token


class CustomAuthMiddleware(AuthMiddleware):

    def __init__(self, inner):
        self.inner = inner

    async def __call__(self, scope, receive, send):
        # Check for token in query parameters
        token = None
        if 'token' in scope['query_string'].decode():
            token = scope['query_string'].decode().split('=')[1]

        if token:
            # Perform token authentication here, you can extract user from the token
            try:
                scope['user'] = await self.get_user(token)
            except Token.DoesNotExist:
                scope['user'] = AnonymousUser()

        return await self.inner(scope, receive, send)

    @database_sync_to_async
    def get_user(self, token):
        try:
            token = Token.objects.get(key=token)
            return token.user
        except Exception as exp:
            print(exp)
            return AnonymousUser()
