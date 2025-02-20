import random
from django.core.mail import send_mail
from django.contrib.auth import authenticate, get_user_model
from rest_framework import serializers
from .models import OTPModel

User = get_user_model()

class UserRegistrationSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True, min_length=6)

    def validate_email(self, email):
        if User.objects.filter(email=email).exists():
            raise serializers.ValidationError("Email is already registered.")
        return email

    def create(self, validated_data):
        email = validated_data['email']

        # Generate OTP
        otp = random.randint(100000, 999999)

        # Save OTP in the database
        OTPModel.objects.create(email=email, otp=otp)

        # Send OTP via email
        send_mail(
            subject="Your OTP Code",
            message=f"Your OTP code is {otp}",
            from_email="your-email@gmail.com",
            recipient_list=[email],
            fail_silently=False,
        )

        return validated_data  # User is not created yet, waits for OTP verification


class VerifyOTPSerializer(serializers.Serializer):
    email = serializers.EmailField()
    otp = serializers.CharField(max_length=6)
    password = serializers.CharField(write_only=True, min_length=6)


class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)

    def validate(self, data):
        email = data.get("email")
        password = data.get("password")
        user = authenticate(username=email, password=password)

        if not user:
            raise serializers.ValidationError("Invalid email or password.")
        
        data["user"] = user
        return data