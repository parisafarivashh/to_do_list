from rest_framework import status
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.generics import CreateAPIView, UpdateAPIView, \
    RetrieveUpdateAPIView
from rest_framework.response import Response

from .models import Token, User
from .serializers import SignUpSerializer, ChangePasswordSerializer, \
    RetrieveUpdateProfileSerializer


class SignUpView(CreateAPIView):
    serializer_class = SignUpSerializer
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)


class SignInView(ObtainAuthToken):
    def post(self, request, *args, **kwargs):
        try:
            serializer = self.serializer_class(data=request.data,
                                               context={'request': request})
            serializer.is_valid(raise_exception=True)
            user = serializer.validated_data['user']
            token = Token.objects.get(user=user)
        except Exception as exp:
            print(exp)
            return Response(status=status.HTTP_401_UNAUTHORIZED)
        return Response(data={'token': token.key}, status=status.HTTP_200_OK)


class ChangePasswordView(UpdateAPIView):
    serializer_class = ChangePasswordSerializer
    permission_classes = [AllowAny]

    def put(self, request, *args, **kwargs):
        username = request.data['username']
        try:
            user = User.objects.get(username=username)
            serializer = self.serializer_class(user, data=request.data)
            serializer.is_valid(raise_exception=True)
            serializer.save()

        except User.DoesNotExist:
            return Response(
                data={'message': 'username dose not exist'},
                status=status.HTTP_400_BAD_REQUEST
            )

        return Response(
            data={'message': 'Password Changed Successfully'},
            status=status.HTTP_200_OK,
        )


class UpdateProfileView(RetrieveUpdateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = RetrieveUpdateProfileSerializer
    queryset = User.objects.all()

    def get_object(self):
        return self.request.user

