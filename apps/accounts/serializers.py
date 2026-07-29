from rest_framework import serializers
from .models import User
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import authenticate

# register serialiser
class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User

        fields = ["id","first_name","last_name","email","phone","password"]



    def create(self, validated_data):

        password = validated_data.pop("password")

        user = User.objects.create_user(
            password=password, **validated_data ) 
        
        user.is_active = False     # Register Serializer
        user.save()

        
        return user
    


# login serializers

class LoginSerializer(serializers.Serializer):
    email=serializers.EmailField()
    password=serializers.CharField(write_only=True)

    def validate(self, attrs):
        email = attrs.get("email")
        password = attrs.get("password")

        user = authenticate(username=email, password=password)

        if not user:
            raise serializers.ValidationError("Invalid Credentials")
        
        refresh = RefreshToken.for_user(user)

        return {
            "refresh": str(refresh),
            "access": str(refresh.access_token),
            "user": {
        "id": user.id,
        "email": user.email,
        "first_name": user.first_name,
        "last_name": user.last_name,
    }
}
    

class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["id", "first_name", "last_name", "email", "phone", "profile_image"]


class ChangePasswordSerializer(serializers.Serializer):
    old_password = serializers.CharField()
    new_password = serializers.CharField()


# Forgot Password Serializer
class ForgotPasswordSerializer(serializers.Serializer):
    email = serializers.EmailField()

# Reset Password serializer
class ResetPasswordSerializer(serializers.Serializer):
    password = serializers.CharField()

