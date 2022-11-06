from django.urls import path

from .views import SignUpView, Login


urlpatterns = [
    path('sign-in/', Login.as_view(), name='api_token_auth'),
    path('sign-up/', SignUpView.as_view()),
]