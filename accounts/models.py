# accounts/models.py

from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    CAISSIER = 'caissier'
    COMPTABLE = 'comptable'
    RESPONSABLE = 'responsable'
    CLIENT = 'client'

    ROLE_CHOICES = [
        (CAISSIER, 'Caissier'),
        (COMPTABLE, 'Comptable'),
        (RESPONSABLE, 'Responsable'),
        (CLIENT, 'Client'),  # Ajout du rôle client
    ]

    role = models.CharField(max_length=20, choices=ROLE_CHOICES)

    def save(self, *args, **kwargs):
        if self.role == 'responsable':
            self.is_staff = True
        super().save(*args, **kwargs)

    def __str__(self):
        return self.username


class UserPreference(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    theme = models.CharField(max_length=50, choices=[('light', 'Clair'), ('dark', 'Sombre')], default='light')
    language = models.CharField(max_length=50, choices=[('fr', 'Français'), ('en', 'Anglais')], default='fr')

    def __str__(self):
        return f"{self.user.username} - Préférences"