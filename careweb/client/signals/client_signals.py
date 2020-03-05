from django.db.models.signals import post_save
from django.dispatch import receiver

from client.models import Client
from client.utils import get_quality_life_number


@receiver(post_save, sender=Client, dispatch_uid="add_ql_code")
def ql_code_signal(instance, created, **kwargs):
    if not instance.lashma_quality_life_no:
        instance.lashma_quality_life_no = get_quality_life_number(instance)
        instance.save()
