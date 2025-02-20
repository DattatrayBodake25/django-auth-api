from django.urls import path
from .views import RegisterView, VerifyOTPView, LoginView, LogoutView, UserDetailsView

urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('register/verify/', VerifyOTPView.as_view(), name='verify-otp'),
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('me/', UserDetailsView.as_view(), name='user-details'),
]