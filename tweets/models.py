from django.db import models
from django.conf import settings
from cloudinary.models import CloudinaryField

class Post(models.Model):
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='posts')
    
    # NOVÉ: Volitelný titulek pro galerii
    title = models.CharField(max_length=100, blank=True, null=True) 
    
    # Obsah (funguje jako běžný tweet nebo jako popis/komentář k fotce v galerii)
    content = models.TextField(max_length=2000, blank=True)
    
    # Fotka (pokud je vyplněna, příspěvek se automaticky ukáže i v galerii uživatele)
    # NOVÉ: Ultimátní Cloudinary pole
    image = CloudinaryField(
        'image', 
        folder='post_images', # Složka přímo na Cloudinary
        format='webp',        # Vynucený moderní formát
        transformation=[
            # Fotka se při uploadu fyzicky zmenší na max šířku 1920px a kvalita se automaticky optimalizuje
            {'width': 1920, 'crop': 'limit', 'quality': 'auto'}
        ],
        blank=True, null=True
    )
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"Post #{self.id} by {self.author.username}"

class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments')
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='comments')
    content = models.TextField(max_length=500)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['created_at']

class Like(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='likes')
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='likes')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'post')