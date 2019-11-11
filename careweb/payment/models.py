from django.db import models
from django.utils import timezone


class Payment(models.Model):
    PENDING = 0
    FAILED = 1
    SUCCESSFUL = 2
    STATUSES = enumerate(("Pending", "Failed", "Successful"))

    amount = models.DecimalField(max_digits=10, decimal_places=2)
    payment_date = models.DateField(default=timezone.now)
    reference = models.CharField(max_length=200, blank=True)
    status = models.PositiveIntegerField(choices=STATUSES, default=PENDING)

    def __str__(self):
        return "{}".format(self.amount)
