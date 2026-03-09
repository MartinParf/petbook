from celery import shared_task
from django.core.mail import send_mail
from django.conf import settings

@shared_task
def send_welcome_email_task(user_email, pet_name):
    """
    Odešle skutečný uvítací e-mail na pozadí přes SMTP server.
    """
    subject = f'Vítejte v Petbooku, {pet_name}!'
    message = (
        f'Ahoj!\n\n'
        f'Jsme nadšeni, že se tvůj mazlíček {pet_name} přidal k naší síti Petbook. '
        f'Připrav se na spoustu sdílení, fotek a nových zvířecích přátel!\n\n'
        f'Tým Petbook'
    )
    
    # Skutečné odeslání e-mailu (Django se postará o spojení s Gmailem/SMTP)
    send_mail(
        subject=subject,
        message=message,
        from_email=settings.EMAIL_HOST_USER,
        recipient_list=[user_email],
        fail_silently=False,  # Pokud to spadne, chceme vidět chybu v Sentry
    )
    
    return f"E-mail úspěšně odeslán na {user_email}"