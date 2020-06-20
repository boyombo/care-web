from provider.models import CareProvider


def is_valid_provider_mail(pid, email):
    if CareProvider.objects.filter(email=email).exists():
        cp = CareProvider.objects.get(email=email)
        return pid and cp.id == pid
    return True
