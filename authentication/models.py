from django.db import models
from django.utils.timezone import now
from datetime import timedelta

class OTPModel(models.Model):
    email = models.EmailField(unique=True)
    otp = models.CharField(max_length=6)
    created_at = models.DateTimeField(auto_now_add=True)  # Track OTP creation time

    def is_expired(self):
        """Check if OTP is expired (valid for 5 minutes)."""
        return now() > self.created_at + timedelta(minutes=5)

    def __str__(self):
        return f"{self.email} - {self.otp}"