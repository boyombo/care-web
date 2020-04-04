from django.contrib.auth.models import Permission
from django.db.models.signals import post_save
from django.dispatch import receiver
from constance import config

from client.models import Client, AdhocClient
from client.utils import get_quality_life_number
from core.utils import send_email

import logging

logger = logging.getLogger(__name__)


@receiver(post_save, sender=Client, dispatch_uid="add_ql_code")
def ql_code_signal(instance, created, **kwargs):
    if not instance.lashma_quality_life_no:
        instance.lashma_quality_life_no = get_quality_life_number(instance)
        instance.save()
    # Check if client limit has been reached and send email
    limit = config.CLIENT_LIMIT
    emails = config.CLIENT_LIMIT_RECEIVERS
    if isinstance(limit, int) and emails:
        if Client.objects.count() >= limit:
            try:
                recipients = str(emails).split(",")
                send_email(recipients, "client_limit_notification", {"total": Client.objects.count()})
                logger.info("Client limit notification sent")
            except Exception as e:
                logger.error("Client limit email failed. Reason: %s" % e)


@receiver(post_save, sender=AdhocClient, dispatch_uid="set_adhoc_permission")
def adhoc_permission_signal(instance, created, **kwargs):
    if not instance.user.has_perm('client.is_adhoc'):
        user = instance.user
        user.user_permissions.add(Permission.objects.get(codename='is_adhoc'))
        user.save()
