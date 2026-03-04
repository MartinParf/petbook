from django.contrib.auth.models import AbstractUser
from cloudinary.models import CloudinaryField
from django.db import models

class CustomUser(AbstractUser):
    # Přidáno pet_type a přejmenováno na pet_name
    pet_type = models.CharField(max_length=50, blank=True) # např. Dog, Cat, Guinea Pig
    pet_name = models.CharField(max_length=50, blank=True) # např. Olivia

    avatar = CloudinaryField(
        'avatar',
        folder='avatars',
        format='webp',
        transformation=[
            {'width': 400, 'height': 400, 'crop': 'fill', 'gravity': 'face', 'quality': 'auto'}
        ],
        blank=True, null=True
    )


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
        # Nyní to v administraci ukáže např.: @olivia_the_brit (Cat - Olivia)
        type_and_name = f" ({self.pet_type} - {self.pet_name})" if self.pet_type or self.pet_name else ""
        return f"@{self.username}{type_and_name}"