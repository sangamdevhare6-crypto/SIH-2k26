from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    ROLE_CHOICES = [('citizen', 'Citizen'), ('admin', 'Administrator')]
    email = models.EmailField(unique=True)
    mobile = models.CharField(max_length=20, blank=True)
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='citizen')
    username = models.CharField(max_length=150, unique=True)

    def __str__(self):
        return f'{self.name_for_display} <{self.email}>'

    @property
    def name_for_display(self):
        return self.get_full_name() or self.username
