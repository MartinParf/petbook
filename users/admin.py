from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser

class CustomUserAdmin(UserAdmin):
    model = CustomUser
    
    # Změněno z 'Cat Profile Details' na univerzální 'Pet Profile Details'
    # a přidáno pole 'pet_type' a 'pet_name'
    fieldsets = UserAdmin.fieldsets + (
        ('Pet Profile Details', {'fields': ('pet_type', 'pet_name', 'avatar', 'bio', 'location')}),
        ('Physical Attributes', {'fields': ('birth_date', 'breed', 'fur_color', 'eye_color')}),
        ('Preferences & Personality', {'fields': ('personality_traits', 'favorite_food', 'favorite_activities')}),
        ('System', {'fields': ('is_verified',)}),
    )

admin.site.register(CustomUser, CustomUserAdmin)