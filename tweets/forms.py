from django import forms
from django.core.exceptions import ValidationError
from .models import Post

class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['title', 'content', 'image']
        
        widgets = {
            'title': forms.TextInput(attrs={'placeholder': 'Photo title (optional)'}),
            'content': forms.Textarea(attrs={'placeholder': 'What is happening? Or describe your photo...'}),
        }

    def clean_image(self):
        image = self.cleaned_data.get('image')
        
        if image:
            # 20 MB limit
            max_size_mb = 20
            if image.size > max_size_mb * 1024 * 1024:
                raise ValidationError(f"Image size exceeds the {max_size_mb}MB limit. Please upload a smaller file.")
            
            # Bezpečnostní kontrola typu souboru
            valid_extensions = ['image/jpeg', 'image/png', 'image/webp', 'image/gif']
            if image.content_type not in valid_extensions:
                raise ValidationError("Invalid file format. Only JPEG, PNG, WEBP, and GIF are allowed.")
                
        return image