import os
from celery import Celery

# Nastavíme výchozí Django settings modul pro Celery program
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'petbook.settings')

# Vytvoříme instanci Celery s názvem projektu
app = Celery('petbook')

# Celery si načte konfiguraci z settings.py (všechny proměnné začínající na CELERY_)
app.config_from_object('django.conf:settings', namespace='CELERY')

# Automaticky najde a načte úkoly ze souborů tasks.py ve všech tvých aplikacích (např. users)
app.autodiscover_tasks()