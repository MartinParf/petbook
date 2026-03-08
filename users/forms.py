from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm, UserChangeForm
from django.core.exceptions import ValidationError
from .models import CustomUser

# Společné CSS třídy pro všechny inputy, aby vypadaly všude naprosto stejně a prémiově
COMMON_INPUT_CLASSES = 'w-full bg-cream dark:bg-softdark border border-cream-dark dark:border-softdark-border text-stone-900 dark:text-white rounded-xl px-4 py-3 focus:outline-none focus:ring-2 focus:ring-accent transition-all'


class CustomUserCreationForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = CustomUser
        # Pro maximální UX rychlost chceme při registraci jen jméno. Hesla si Django přidá samo. Test
        #fields = ('username',) # zde zakomentováno, aby se přidalo více polí
        fields = ('username', 'email', 'pet_name', 'pet_type')
        
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs.update({'class': COMMON_INPUT_CLASSES})

        self.fields['email'].widget.attrs.update({'placeholder': 'you@example.com'})

class CustomAuthenticationForm(AuthenticationForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs.update({'class': COMMON_INPUT_CLASSES})

class UserProfileForm(forms.ModelForm):
    class Meta:
        model = CustomUser
        # Vybereme jen pole, která chceme, aby si uživatel mohl sám upravit
        fields = [
            'pet_name', 'pet_type', 'avatar', 'bio', 'location', 
            'birth_date', 'breed', 'fur_color', 'eye_color', 
            'personality_traits', 'favorite_food', 'favorite_activities'
        ]
        
        # Přidáme nápovědy a placeholder pro lepší UX
        widgets = {
            'bio': forms.Textarea(attrs={'rows': 3, 'placeholder': 'Tell us about your pet...'}),
            'birth_date': forms.DateInput(attrs={'type': 'date'}), # Vynutí HTML5 kalendář
            'personality_traits': forms.TextInput(attrs={'placeholder': 'quiet, shy, shedding a lot...'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Automatické vstříknutí CSS tříd do všech polí
        for field_name, field in self.fields.items():
            # Speciální třída pro pole souboru (Avatar), aby nebylo ošklivé
            if isinstance(field.widget, forms.FileInput):
                field.widget.attrs.update({'class': 'w-full text-stone-600 dark:text-stone-400 file:mr-4 file:py-2 file:px-4 file:rounded-full file:border-0 file:text-sm file:font-semibold file:bg-accent file:text-white hover:file:bg-accent-hover cursor-pointer'})
            else:
                field.widget.attrs.update({'class': COMMON_INPUT_CLASSES})

    # BEZPEČNOST: Kontrola nahraného Avatara
    def clean_avatar(self):
        avatar = self.cleaned_data.get('avatar')
        if avatar:
            # 20 MB limit pro Avatara
            max_size_mb = 20
            if avatar.size > max_size_mb * 1024 * 1024:
                raise ValidationError(f"Avatar is too large. Maximum size is {max_size_mb}MB.")
            
            # Whitelist typů souborů
            valid_extensions = ['image/jpeg', 'image/png', 'image/webp', 'image/gif']
            if avatar.content_type not in valid_extensions:
                raise ValidationError("Invalid format. Please upload JPEG, PNG, WEBP, or GIF.")
        return avatar