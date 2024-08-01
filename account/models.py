import uuid
import os
from django.contrib.auth.models import AbstractUser, PermissionsMixin
from django.conf import settings
from django.db import models
from django.utils import timezone
from datetime import timedelta

class User(AbstractUser, PermissionsMixin):
    email = models.EmailField(unique=True)
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    def __str__(self):
        return self.username
    

class AuthUserToken(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    expires_at = models.DateTimeField(null=True, blank=True)

    def save(self, *args, **kwargs):
        if not self.expires_at:
            self.expires_at = timezone.now() + timedelta(days=int(os.getenv('RAUM_TOKEN_TIMEOUT', 90)))
        super().save(*args, **kwargs)

    def __str__(self):
        return str(self.id)

    @property
    def is_expired(self):
        return timezone.now() >= self.expires_at
    
