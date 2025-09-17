from django.db import models
from django.contrib.auth.models import User

# Create your models here.


class Profile(models.Model):
    ROLE_CHOICES = [
        ("chef", "Chef"),
        ("manager", "Manager"),
        ("staff", "Staff"),
    ]
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default="staff")
    # Add more profile fields as needed (e.g., phone, avatar, etc.)

    def __str__(self):
        return f"{self.user.username} ({self.get_role_display()})"

    def get_role_display(self):
        return dict(self.ROLE_CHOICES).get(self.role, "Staff")


# OTP model for one-time password functionality
import uuid
from django.utils import timezone

class OneTimePassword(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    code = models.CharField(max_length=12, unique=True, default=uuid.uuid4)
    created_at = models.DateTimeField(auto_now_add=True)
    used = models.BooleanField(default=False)
    used_at = models.DateTimeField(null=True, blank=True)

    def mark_used(self):
        self.used = True
        self.used_at = timezone.now()
        self.save()

    def __str__(self):
        return f"OTP for {self.user.username} ({'used' if self.used else 'unused'})"
