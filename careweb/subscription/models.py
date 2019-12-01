from django.db import models
from django.utils import timezone

from client.models import Client, Dependant
from ranger.models import Ranger
from payment.models import Payment
from core.models import Plan


class Subscription(models.Model):
    client = models.ForeignKey(Client, on_delete=models.CASCADE)
    subscribed_on = models.DateTimeField(default=timezone.now)
    start_date = models.DateField(null=True)
    expiry_date = models.DateField()
    plan = models.ForeignKey(Plan, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    active = models.BooleanField(default=True)
    next_subscription = models.ForeignKey("self", null=True, on_delete=models.SET_NULL)
    dependants = models.ManyToManyField(Dependant)

    def __str__(self):
        return str(self.client)


class SubscriptionPayment(models.Model):
    PENDING = 0
    FAILED = 1
    SUCCESSFUL = 2
    STATUSES = enumerate(("Pending", "Failed", "Successful"))

    BANK_TRANSFER = 0
    BANK_DEPOSIT = 1
    CARD = 2
    PAYMENT_TYPES = enumerate(("Bank Transfer", "Bank Deposit", "Card"))

    client = models.ForeignKey(Client, on_delete=models.CASCADE)
    payment_date = models.DateField(default=timezone.now)
    payment = models.ForeignKey(Payment, null=True, on_delete=models.SET_NULL)
    payment_type = models.PositiveIntegerField(
        choices=PAYMENT_TYPES, default=BANK_TRANSFER
    )
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    bank = models.CharField(max_length=100, null=True, blank=True)
    name = models.CharField(max_length=100, null=True, blank=True)
    status = models.PositiveIntegerField(choices=STATUSES, default=PENDING)
    rejection_reason = models.TextField(null=True, blank=True)
    ranger = models.ForeignKey(Ranger, null=True, blank=True, on_delete=models.SET_NULL)

    def __str__(self):
        return str(self.client)
