from django.contrib.auth.models import AbstractUser
from django.db import models

class CustomUser(AbstractUser):
    # Základní profil (Basic Profile)
    cat_name = models.CharField(max_length=50, blank=True) # např. Olivia
    avatar = models.ImageField(upload_to='avatars/', blank=True, null=True)
    bio = models.TextField(max_length=500, blank=True)
    location = models.CharField(max_length=100, blank=True) # např. Edinburgh
    
    # Fyzické vlastnosti (Physical Attributes)
    birth_date = models.DateField(null=True, blank=True) # Z tohoto spočítáme těch 7 let
    breed = models.CharField(max_length=100, blank=True) # např. British Shorthair
    fur_color = models.CharField(max_length=50, blank=True) # např. Brown
    eye_color = models.CharField(max_length=50, blank=True) # např. Brown
    
    # Povaha a preference (Personality & Preferences)
    personality_traits = models.CharField(max_length=200, blank=True) # např. quiet, shy, sheds a lot
    favorite_food = models.CharField(max_length=100, blank=True) # např. canned fish
    favorite_activities = models.CharField(max_length=200, blank=True) # např. long petting, brushing
    
    # Systémové flagy (System Flags)
    is_verified = models.BooleanField(default=False)

    def __str__(self):
        # Vrátí například: @olivia_the_brit (Olivia)
        name_display = f" ({self.cat_name})" if self.cat_name else ""
        return f"@{self.username}{name_display}"