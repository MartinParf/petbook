from django.shortcuts import render, redirect, get_object_or_404
from django.core.paginator import Paginator
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_GET
from django_ratelimit.decorators import ratelimit
from django.contrib.auth import get_user_model
from .models import Post
from .forms import PostForm

User = get_user_model()

# 1. HLAVNÍ ZEĎ (Vidí všichni, i nepřihlášení)
@require_GET
def feed_view(request):
    # Vybere všechny příspěvky. Optimalizace přes select_related načte autory hned.
    # prefetch_related načte rovnou počet lajků a komentářů, aniž by zahltil databázi.
    posts = Post.objects.select_related('author').prefetch_related('likes', 'comments').all()
    
    paginator = Paginator(posts, 3) # 3 příspěvky na stránku, změněno z 20
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    return render(request, 'tweets/feed.html', {'page_obj': page_obj})

# 2. GALERIE UŽIVATELE (Vidí všichni)
@require_GET
def user_gallery_view(request, username):
    target_user = get_object_or_404(User, username=username)
    
    # MAGIE: Vybereme pouze příspěvky tohoto uživatele, které MAJÍ OBRÁZEK
    photos = Post.objects.filter(author=target_user).exclude(image='').select_related('author').prefetch_related('likes', 'comments')
    
    paginator = Paginator(photos, 30) # V galerii ukážeme 30 fotek na stránku
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    return render(request, 'tweets/gallery.html', {
        'target_user': target_user,
        'page_obj': page_obj
    })

# 3. PŘIDÁNÍ PŘÍSPĚVKU / FOTKY DO GALERIE (Jen přihlášení, omezení rychlosti proti spamu)
@login_required(login_url='/users/login/')
@ratelimit(key='ip', rate='10/m', block=True)
def create_post_view(request):
    if request.method == 'POST':
        # Důležité: 'request.FILES' zpracovává nahrávané obrázky z formuláře
        form = PostForm(request.POST, request.FILES)
        if form.is_valid():
            # Neuložíme hned do databáze, musíme přiřadit autora!
            new_post = form.save(commit=False)
            new_post.author = request.user
            new_post.save()
            
            # Pokud nahrál obrázek, přesměrujeme ho do jeho galerie, jinak na zeď
            if new_post.image:
                return redirect('tweets:user_gallery', username=request.user.username)
            return redirect('tweets:feed')
    else:
        form = PostForm()
        
    return render(request, 'tweets/create_post.html', {'form': form})