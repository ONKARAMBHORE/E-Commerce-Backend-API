from django.urls import path

from .views import ForgotPasswordView, RegisterView, ResetPasswordView, VerifyEmailView
from .views import LoginView
from .views import LogoutView
from .views import ProfileView
from .views import ChangePasswordView
from rest_framework_simplejwt.views import (
    TokenRefreshView
)


urlpatterns = [

    path("register/",RegisterView.as_view(),name="register"),

    path("login/", LoginView.as_view(), name="login"),

    path("logout/", LogoutView.as_view(), name="logout"),
    path("profile/", ProfileView.as_view(), name="profile"),
    path("change-password/", ChangePasswordView.as_view(), name="change-password"),
    path("refresh/", TokenRefreshView.as_view(), name="refresh"),
    path("forgot-password/", ForgotPasswordView.as_view(), name="forgot-password"),
    path("reset-password/<uid>/<token>/", ResetPasswordView.as_view(), name="reset-password"),
    path("verify-email/<uid>/<token>/", VerifyEmailView.as_view(), name="verify-email"),

]