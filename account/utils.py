import os
from ninja.security import HttpBearer
from .models import AuthUserToken


def get_or_create_token(user):
    try:
        token = AuthUserToken.objects.get(user=user)
        if token.is_expired:
            token.delete()
            token = AuthUserToken.objects.create(user=user)
    except AuthUserToken.DoesNotExist:
        token = AuthUserToken.objects.create(user=user)
    return token

def verify_email_domains(email):
    email_domains = os.getenv('RAUM_ALLOWED_EMAIL_DOMAINS')
    domain_list = email_domains.split(",")
    user_email_domain = email.split('@')[1]
    if user_email_domain in domain_list:
        return True
    else:
        return False


class AuthBearer(HttpBearer):
    def authenticate(self, request, token):
        try:
            token = AuthUserToken.objects.get(id=token)
            if token.is_expired:
                return None
            return token.user
        except AuthUserToken.DoesNotExist:
            return None
        