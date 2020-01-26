from django.db import models
from django.utils import timezone

from hashid_field import HashidAutoField


class Payment(models.Model):
    PENDING = 0
    FAILED = 1
    SUCCESSFUL = 2
    STATUSES = enumerate(("Pending", "Failed", "Successful"))

    BANK_PAYMENT = 0
    CARD_PAYMENT = 1
    FUND_REQUEST = 2
    MODES = enumerate(("Bank", "Card", "Fund Request"))

    id = HashidAutoField(primary_key=True)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    payment_date = models.DateField(default=timezone.now)
    reference = models.CharField(max_length=200, blank=True)
    cust_reference = models.CharField(max_length=200, blank=True)
    status = models.PositiveIntegerField(choices=STATUSES, default=PENDING)
    payment_mode = models.PositiveIntegerField(choices=MODES, null=True)
    narration = models.TextField(blank=True, null=True)
    paid_by = models.CharField(max_length=200, blank=True)

    def __str__(self):
        return "{}".format(self.amount)
