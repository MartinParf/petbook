from django.shortcuts import render, redirect
from django.contrib.auth import login, logout
from django_ratelimit.decorators import ratelimit
from .forms import CustomUserCreationForm, CustomAuthenticationForm, UserProfileForm
from django.contrib.auth.decorators import login_required
from .tasks import send_welcome_email_task  # <-- Importujeme náš úkol

# OMEZENÍ: Z jedné IP adresy max 5 pokusů o registraci za hodinu (Zastaví botnety)
@ratelimit(key='ip', rate='5/h', block=True)
def register_view(request):
    if request.user.is_authenticated:
        return redirect('tweets:feed')

    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            
            # MAGIE: Odpálíme úkol na pozadí! 
            # Funkce okamžitě pokračuje dál, nečeká na výsledek.
            send_welcome_email_task.delay(user.email, user.pet_name)

            # TADY JE TA OPRAVA: Natvrdo řekneme, jaký backend se má pro relaci použít
            login(request, user, backend='users.backends.EmailOrUsernameModelBackend')
            
            return redirect('tweets:feed')
    else:
        form = CustomUserCreationForm()
        
    return render(request, 'users/register.html', {'form': form})

# OMEZENÍ: Max 10 pokusů o přihlášení za minutu (Zastaví útoky hrubou silou na hesla)
@ratelimit(key='ip', rate='10/m', block=True)
def login_view(request):
    if request.user.is_authenticated:
        return redirect('tweets:feed')

    if request.method == 'POST':
        form = CustomAuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('tweets:feed')
    else:
        form = CustomAuthenticationForm()
        
    return render(request, 'users/login.html', {'form': form})

# Odhlášení
def logout_view(request):
    logout(request)
    return redirect('tweets:feed')

# 1. Musí být přihlášen
# 2. OMEZENÍ: Max 10 uložení profilu za minutu (Zastaví spamování API)
@login_required(login_url='users:login')
@ratelimit(key='user', rate='10/m', block=True)
def edit_profile_view(request):
    # DŮLEŽITÉ: instance=request.user – naplníme formulář daty přihlášeného uživatele
    if request.method == 'POST':
        # Nezapomeň na request.FILES pro zpracování nového Avatara!
        form = UserProfileForm(request.POST, request.FILES, instance=request.user)
        if form.is_valid():
            form.save()
            # Přesměrujeme ho do jeho vlastní galerie
            return redirect('tweets:user_gallery', username=request.user.username)
    else:
        form = UserProfileForm(instance=request.user)
        
    return render(request, 'users/edit_profile.html', {'form': form})