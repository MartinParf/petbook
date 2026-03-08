from django.contrib.auth.backends import ModelBackend
from django.contrib.auth import get_user_model
from django.db.models import Q

User = get_user_model()

class EmailOrUsernameModelBackend(ModelBackend):
    def authenticate(self, request, username=None, password=None, **kwargs):
        if username is None:
            username = kwargs.get(User.USERNAME_FIELD)
        try:
            # Hledáme uživatele: buď se vstup rovná username, NEBO emailu
            user = User.objects.get(Q(username__iexact=username) | Q(email__iexact=username))
        except User.DoesNotExist:
            # Bezpečnostní trik proti hackerům (aby nezjistili, že e-mail existuje)
            User().set_password(password)
            return None

        # Pokud uživatele najdeme, ověříme heslo
        if user.check_password(password) and self.user_can_authenticate(user):
            return user
            
        return None