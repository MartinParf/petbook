from django.urls import path
from . import views

app_name = 'tweets' # Jmenný prostor pro bezpečné odkazování v HTML šablonách

urlpatterns = [
    # 1. Hlavní zeď (Feed) - dostupná na hlavní stránce webu (např. tvujweb.cz/)
    path('', views.feed_view, name='feed'),
    
    # 2. Formulář pro nový příspěvek/fotku - dostupný na tvujweb.cz/post/new/
    path('post/new/', views.create_post_view, name='create_post'),
    
    # 3. Kočičí galerie - dynamická URL, kde <str:username> zachytí jméno kočky
    # Příklad: tvujweb.cz/gallery/olivia_the_brit/
    path('gallery/<str:username>/', views.user_gallery_view, name='user_gallery'),

    # NOVÉ CESTY PRO LAJKY A KOMENTÁŘE
    path('post/<int:post_id>/like/', views.toggle_like_view, name='toggle_like'),
    path('post/<int:post_id>/comment/', views.add_comment_view, name='add_comment'),
    path('post/<int:post_id>/delete/', views.delete_post_view, name='delete_post'),
    path('comment/<int:comment_id>/delete/', views.delete_comment_view, name='delete_comment'),

]