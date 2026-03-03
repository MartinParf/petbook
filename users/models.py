from django.contrib.auth.models import AbstractUser
from django.db import models

class CustomUser(AbstractUser):
    cat_name = models.CharField(max_length=50, blank=True)
    avatar = models.ImageField(upload_to='avatars/', blank=True, null=True)
    bio = models.TextField(max_length=500, blank=True)
    location = models.CharField(max_length=100, blank=True)
    
    birth_date = models.DateField(null=True, blank=True)
    breed = models.CharField(max_length=100, blank=True)
    fur_color = models.CharField(max_length=50, blank=True)
    eye_color = models.CharField(max_length=50, blank=True)
    
    personality_traits = models.CharField(max_length=200, blank=True)
    favorite_food = models.CharField(max_length=100, blank=True)
    favorite_activities = models.CharField(max_length=200, blank=True)
    
    is_verified = models.BooleanField(default=False)

    def __str__(self):
        return f"@{self.username}"