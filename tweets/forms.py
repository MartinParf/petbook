from django import forms
from django.core.exceptions import ValidationError
from .models import Post

# Společné třídy pro dark mode a zaoblený design
COMMON_INPUT_CLASSES = 'w-full bg-cream dark:bg-softdark border border-cream-dark dark:border-softdark-border text-stone-900 dark:text-white rounded-xl px-4 py-3 focus:outline-none focus:ring-2 focus:ring-accent transition-all'

class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['content', 'image'] # Smazán 'title'
        
        widgets = {
            'title': forms.TextInput(attrs={'placeholder': 'Photo title (optional)'}),
            'content': forms.Textarea(attrs={'placeholder': 'What is happening? Or describe your photo...'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Šetrné přidání Tailwind CSS tříd bez narušení tvých placeholderů
        for field_name, field in self.fields.items():
            if isinstance(field.widget, forms.FileInput):
                # Design pro tlačítko "Vybrat soubor"
                field.widget.attrs.update({'class': 'w-full text-stone-600 dark:text-stone-400 file:mr-4 file:py-2 file:px-4 file:rounded-full file:border-0 file:text-sm file:font-semibold file:bg-accent file:text-white hover:file:bg-accent-hover cursor-pointer'})
            else:
                # Aplikace Dark Mode barev na title a content
                field.widget.attrs.update({'class': COMMON_INPUT_CLASSES})

    def clean_image(self):
        image = self.cleaned_data.get('image')
        
        # Bezpečnostní pojistka: Kontroluj jen nové soubory z PC (mají atribut 'size')
        if image and hasattr(image, 'size'):
            # 20 MB limit
            max_size_mb = 20
            if image.size > max_size_mb * 1024 * 1024:
                raise ValidationError(f"Image size exceeds the {max_size_mb}MB limit. Please upload a smaller file.")
            
            # Bezpečnostní kontrola typu souboru
            valid_extensions = ['image/jpeg', 'image/png', 'image/webp', 'image/gif']
            if hasattr(image, 'content_type') and image.content_type not in valid_extensions:
                raise ValidationError("Invalid file format. Only JPEG, PNG, WEBP, and GIF are allowed.")
                
        return image