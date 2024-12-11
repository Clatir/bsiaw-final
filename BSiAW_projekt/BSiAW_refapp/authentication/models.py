from django.contrib.auth.models import User
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver


class UserProfile(models.Model):
    ROLE_CHOICES = [
        ('ref', 'Sędzia'),
        ('kol', 'Kolegium'),
    ]

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    role = models.CharField(max_length=50, default='user')
   
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='undefined', unique=False)
    otp_enabled = models.BooleanField(default=False)  # Czy OTP jest włączone

    
    def is_judge(self):
        return self.role == 'judge'

    def is_committee(self):
        return self.role == 'committee'
    