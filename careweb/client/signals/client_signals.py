from django.contrib.auth.models import Permission
from django.db.models.signals import post_save
from django.dispatch import receiver

from client.models import Client, AdhocClient
from client.utils import get_quality_life_number


@receiver(post_save, sender=Client, dispatch_uid="add_ql_code")
def ql_code_signal(instance, created, **kwargs):
    if not instance.lashma_quality_life_no:
        instance.lashma_quality_life_no = get_quality_life_number(instance)
        instance.save()


@receiver(post_save, sender=AdhocClient, dispatch_uid="set_adhoc_permission")
def adhoc_permission_signal(instance, created, **kwargs):
    if not instance.user.has_perm('client.is_adhoc'):
        user = instance.user
        user.user_permissions.add(Permission.objects.get(codename='is_adhoc'))
        user.save()
