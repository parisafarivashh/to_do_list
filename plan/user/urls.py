from django.urls import path

from .views import SignUpView, SignInView, ChangePasswordView

urlpatterns = [
    path('sign-in/', SignInView.as_view(), name='sign_in'),
    path('sign-up/', SignUpView.as_view(), name='sign_up'),
    path('change-password/', ChangePasswordView.as_view(), name='change_password'),
]