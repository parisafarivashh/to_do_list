from rest_framework import status
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.permissions import AllowAny
from rest_framework.generics import CreateAPIView
from rest_framework.response import Response

from .models import Token
from .serializers import SignUpSerializer


class SignUpView(CreateAPIView):
    serializer_class = SignUpSerializer
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(serializer.data, status=status.HTTP_200_OK)


class Login(ObtainAuthToken):
    def post(self, request, *args, **kwargs):
        try:
            serializer = self.serializer_class(data=request.data,
                                               context={'request': request})
            serializer.is_valid(raise_exception=True)
            user = serializer.validated_data['user']
            token = Token.objects.get(user=user)
        except:
            return Response(status=status.HTTP_401_UNAUTHORIZED)
        return Response({'token': token.key})
