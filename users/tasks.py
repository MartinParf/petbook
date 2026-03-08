from celery import shared_task
import time

@shared_task
def send_welcome_email_task(user_email, pet_name):
    """
    Tento úkol běží na pozadí, mimo hlavní Django vlákno.
    """
    print(f"CELERY ZAČÍNÁ: Připravuji uvítací e-mail pro {pet_name} ({user_email})...")
    
    # Simulujeme zdržení (např. komunikace se SendGrid / Gmail serverem)
    time.sleep(5) 
    
    # Tady v budoucnu bude skutečný kód pro odeslání e-mailu:
    # send_mail(...)
    
    print(f"CELERY HOTOVO: E-mail úspěšně odeslán na {user_email}!")
    return True