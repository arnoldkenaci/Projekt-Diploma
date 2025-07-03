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
