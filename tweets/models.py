from django.db import models
from django.conf import settings

# 1. TABULKA PŘÍSPĚVKŮ (Posts/Tweets)
class Post(models.Model):
    # Propojení na uživatele: Když se smaže uživatel, smažou se i jeho příspěvky (CASCADE)
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='posts')
    content = models.TextField(max_length=2000)
    
    # Obrázek nahraný do Cloudinary (volitelný)
    image = models.ImageField(upload_to='post_images/', blank=True, null=True)
    
    # Automatická časová razítka
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        # Tímto říkáme Djangu: Vždy řaď příspěvky od nejnovějšího po nejstarší (znaménko mínus)
        ordering = ['-created_at']

    def __str__(self):
        return f"Post by {self.author.username} at {self.created_at.strftime('%Y-%m-%d %H:%M')}"

# 2. TABULKA KOMENTÁŘŮ
class Comment(models.Model):
    # Komentář musí patřit ke konkrétnímu příspěvku a konkrétnímu autorovi
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments')
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='comments')
    content = models.TextField(max_length=500)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        # Komentáře naopak řadíme od nejstaršího po nejnovější (klasická diskuze)
        ordering = ['created_at']

    def __str__(self):
        return f"Comment by {self.author.username} on Post #{self.post.id}"

# 3. TABULKA LAJKŮ
class Like(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='likes')
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='likes')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        # Extrémně důležité zabezpečení databáze: 
        # Jeden uživatel může dát lajk jednomu příspěvku pouze jednou.
        unique_together = ('user', 'post')

    def __str__(self):
        return f"@{self.user.username} likes Post #{self.post.id}"