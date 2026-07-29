
from rest_framework.generics import CreateAPIView
from rest_framework.permissions import AllowAny
from .models import User
from .serializers import RegisterSerializer, ResetPasswordSerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from .serializers import LoginSerializer
from rest_framework.generics import GenericAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken
from .serializers import (
    LoginSerializer,
    UserProfileSerializer,
    ChangePasswordSerializer
)
from apps.notifications.models import Notification
from apps.notifications.utils import send_notification_email
from apps.notifications.utils import send_notification_email




class RegisterView(APIView):

    permission_classes = [AllowAny]

    def post(self, request):

        serializer = RegisterSerializer(data=request.data)

        serializer.is_valid(raise_exception=True)

        user = serializer.save()   # -- After the user is created

        # Welcome Notification
        Notification.objects.create(
            user=user,
            title="Welcome",
            message="Your account has been created successfully."
        )
        # welcome email send by the user 
        # Welcome Email
        send_notification_email(
            "Welcome",
            f"Welcome {user.first_name}! Your account has been created successfully.",
            user.email
        )


        uid = urlsafe_base64_encode(force_bytes(user.pk))

        token = default_token_generator.make_token(user)

        link = f"http://127.0.0.1:8000/api/accounts/verify-email/{uid}/{token}/"

# along with link it send the notification of the email 

        send_notification_email(
            "Verify Email",
            f"Click below link to verify your email.\n{link}",
            user.email
        )


        return Response(
            {
                "message": "Verification Email Sent"
            },
            status=status.HTTP_201_CREATED
        )


class LoginView(GenericAPIView):
    serializer_class = LoginSerializer
    permission_classes = []
    
    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        return Response(serializer.validated_data)



class ProfileView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        serializer = UserProfileSerializer(request.user)
        return Response(serializer.data)
    
    def put(self, request):
        serializer = UserProfileSerializer(request.user, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)
    
# change password
class ChangePasswordView(APIView):
    permission_classes = [IsAuthenticated]

    def put(self, request):
        serializer = ChangePasswordSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        user = request.user

        if not user.check_password(serializer.validated_data["old_password"]):
            return Response(
                {"message": "Old Password Incorrect"},
                status=400
            )

        user.set_password(serializer.validated_data["new_password"])
        user.save()

        return Response(
            {"message": "Password Changed Successfully"}
        )

# logout api 
class LogoutView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        try:
            refresh_token = request.data["refresh"]
            token = RefreshToken(refresh_token)
            token.blacklist()

            return Response(
                {"message": "Logout Successful"}
            )

        except:
            return Response(
                {"message": "Invalid Token"},
                status=400
            )
        

# Forgot Password API

from .serializers import ForgotPasswordSerializer
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.shortcuts import get_object_or_404
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes
from django.core.mail import send_mail
from django.utils.http import urlsafe_base64_decode
from django.utils.encoding import force_str




class ForgotPasswordView(APIView):
    permission_class = []  # Allow anyone to access this API (Forgot Password doesn't require login)

    def post(self, request):  # Handle POST request for forgot password
        serializer = ForgotPasswordSerializer(data=request.data)  # Load request data into serializer

        serializer.is_valid(raise_exception=True)  # Validate email; raise error if invalid

        email = serializer.validated_data["email"]  # Get the validated email from request

        user = get_object_or_404(User, email=email)  # Find user by email or return 404 if not found

        uid = urlsafe_base64_encode(force_bytes(user.pk))  # Encode user ID safely for use in URL

        token = PasswordResetTokenGenerator().make_token(user)  # Generate a secure password reset token

        link = f"http://127.0.0.1:8000/api/accounts/reset-password/{uid}/{token}/"  # Create password reset URL

        send_notification_email(
            "Reset Password",
            f"Click the reset link:\n{link}",
            user.email
        )

        return Response({"message": "Password Reset Link Sent"})  # Return success response

#  reset password api

class ResetPasswordView(APIView):
    permission_classes = []  # Allow anyone to access this API (Reset Password doesn't require login)

    def post(self, request, uid, token):  # Handle POST request for resetting password

        serializer = ResetPasswordSerializer(data=request.data)  # Load request data into serializer

        serializer.is_valid(raise_exception=True)  # Validate the new password

        id = force_str(urlsafe_base64_decode(uid))  # Decode the encoded user ID from the URL

        user = User.objects.get(pk=id)  # Fetch the user using the decoded user ID

        if not PasswordResetTokenGenerator().check_token(user, token):  # Verify whether the reset token is valid

            return Response(
                {"message": "Invalid Token"},  # Return error if token is invalid or expired
                status=400
            )

        user.set_password(serializer.validated_data["password"])  # Hash and set the new password

        user.save()  # Save the updated password in the database

        return Response(
            {"message": "Password Reset Successfully"}  # Return success response after password reset
        )
    


# verify email API 

from django.contrib.auth.tokens import default_token_generator


class VerifyEmailView(APIView):
    permission_classes = []

    def get(self, request, uid, token):
        id = force_str(urlsafe_base64_decode(uid))
        user = User.objects.get(pk=id)

        if default_token_generator.check_token(user, token):
            user.is_verified = True
            user.is_active = True
            user.save()
            return Response({"message": "Email Verified"})

        return Response({"message": "Invalid Link"}, status=400)