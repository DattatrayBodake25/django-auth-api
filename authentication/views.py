from django.contrib.auth import login, logout, get_user_model
from django.middleware.csrf import get_token
from django.core.exceptions import ObjectDoesNotExist
from django.utils.timezone import now
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.authentication import SessionAuthentication
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from datetime import timedelta

from .models import OTPModel
from .serializers import UserRegistrationSerializer, VerifyOTPSerializer, LoginSerializer

User = get_user_model()


class RegisterView(APIView):
    permission_classes = [AllowAny]

    @swagger_auto_schema(
        request_body=UserRegistrationSerializer,
        responses={201: "OTP sent to email for verification."}
    )
    def post(self, request):
        serializer = UserRegistrationSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()  # OTP is sent but user is not created yet
            return Response({"message": "OTP sent to email for verification."}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class VerifyOTPView(APIView):
    permission_classes = [AllowAny]

    @swagger_auto_schema(
        request_body=VerifyOTPSerializer,
        responses={201: "User verified and registered successfully!"}
    )
    def post(self, request):
        serializer = VerifyOTPSerializer(data=request.data)
        if serializer.is_valid():
            email = serializer.validated_data['email']
            otp = serializer.validated_data['otp']
            password = serializer.validated_data['password']

            # Delete expired OTPs
            OTPModel.objects.filter(created_at__lt=now() - timedelta(minutes=5)).delete()

            try:
                otp_entry = OTPModel.objects.get(email=email, otp=otp)

                # Check if OTP is expired
                if otp_entry.is_expired():
                    otp_entry.delete()
                    return Response({"error": "OTP has expired. Please request a new one."}, status=status.HTTP_400_BAD_REQUEST)

                # Create user if OTP is valid
                user = User.objects.create_user(username=email, email=email, password=password)
                otp_entry.delete()  # OTP used, remove it
                return Response({"message": "User verified and registered successfully!"}, status=status.HTTP_201_CREATED)

            except ObjectDoesNotExist:
                return Response({"error": "Invalid OTP or email"}, status=status.HTTP_400_BAD_REQUEST)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class LoginView(APIView):
    permission_classes = [AllowAny]

    @swagger_auto_schema(
        request_body=LoginSerializer,
        responses={200: "Login successful!"}
    )
    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.validated_data["user"]
            login(request, user)

            response = Response({"message": "Login successful!"}, status=status.HTTP_200_OK)
            response.set_cookie(
                key="auth_token",
                value=user.id,  # Here we store user ID as a token (better to use JWT in production)
                httponly=True,
                secure=True,  # Set to True in production with HTTPS
                samesite="Lax"
            )
            response.set_cookie("csrftoken", get_token(request), httponly=False)

            return response
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class LogoutView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        logout(request)
        response = Response({"message": "Logout successful!"}, status=status.HTTP_200_OK)
        response.delete_cookie("auth_token")
        return response


class UserDetailsView(APIView):
    authentication_classes = [SessionAuthentication]  # Using cookie-based authentication
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        return Response({
            "username": user.username,
            "email": user.email,
        }, status=status.HTTP_200_OK)