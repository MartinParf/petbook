from django.urls import path
from . import views

app_name = 'users'

urlpatterns = [
    # Stávající cesty...
    path('register/', views.register_view, name='register'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    
    # NOVÉ: Cesta k úpravě profilu
    path('profile/edit/', views.edit_profile_view, name='edit_profile'),
]