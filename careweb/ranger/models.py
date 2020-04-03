from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

from hashid_field import HashidAutoField
from simple_history.models import HistoricalRecords

from location.models import LGA
from payment.models import Payment


class Ranger(models.Model):
    id = HashidAutoField(primary_key=True)
    user = models.ForeignKey(User, null=True, blank=True, on_delete=models.SET_NULL)
    first_name = models.CharField(max_length=200)
    last_name = models.CharField(max_length=200)
    phone = models.CharField(max_length=50)
    lga = models.ForeignKey(LGA, null=True, on_delete=models.SET_NULL)
    balance = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    created = models.DateTimeField(auto_now_add=True)

    history = HistoricalRecords()

    def __str__(self):
        return "{} {}".format(self.first_name, self.last_name)

    @property
    def username(self):
        return self.user.username


class WalletFunding(models.Model):
    PENDING = 0
    FAILED = 1
    SUCCESSFUL = 2
    STATUSES = enumerate(("Pending", "Failed", "Successful"))

    BANK_TRANSFER = 0
    BANK_DEPOSIT = 1
    PAYSTACK = 2
    PAYMENT_TYPE = enumerate(("Bank Transfer", "Bank Deposit", "Paystack"))

    id = HashidAutoField(primary_key=True)
    ranger = models.ForeignKey(Ranger, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    bank = models.CharField(max_length=100, null=True, blank=True)
    name = models.CharField(max_length=100, null=True, blank=True)
    reference = models.CharField(max_length=100, null=True, blank=True)
    payment_date = models.DateField(default=timezone.now)
    payment_type = models.PositiveIntegerField(
        choices=PAYMENT_TYPE, default=BANK_TRANSFER
    )
    payment = models.ForeignKey(Payment, null=True, on_delete=models.SET_NULL)
    status = models.PositiveIntegerField(choices=STATUSES, default=PENDING)
    rejection_reason = models.TextField(null=True, blank=True)

    history = HistoricalRecords()

    def __str__(self):
        return str(self.ranger)

    class Meta:
        ordering = ["-payment_date"]
