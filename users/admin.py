from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser

class CustomUserAdmin(UserAdmin):
    model = CustomUser
    
    # Rozdělení do přehledných sekcí v Django administraci
    fieldsets = UserAdmin.fieldsets + (
        ('Cat Profile Details', {'fields': ('cat_name', 'avatar', 'bio', 'location')}),
        ('Physical Attributes', {'fields': ('birth_date', 'breed', 'fur_color', 'eye_color')}),
        ('Preferences & Personality', {'fields': ('personality_traits', 'favorite_food', 'favorite_activities')}),
        ('System', {'fields': ('is_verified',)}),
    )

admin.site.register(CustomUser, CustomUserAdmin)