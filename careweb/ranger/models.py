from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

from location.models import LGA
from payment.models import Payment


class Ranger(models.Model):
    user = models.ForeignKey(User, null=True, blank=True, on_delete=models.SET_NULL)
    first_name = models.CharField(max_length=200)
    last_name = models.CharField(max_length=200)
    phone = models.CharField(max_length=50)
    lga = models.ForeignKey(LGA, null=True, on_delete=models.SET_NULL)
    balance = models.DecimalField(max_digits=10, decimal_places=2, default=0)

    def __str__(self):
        return "{} {}".format(self.first_name, self.last_name)


class WalletFunding(models.Model):
    PENDING = 0
    FAILED = 1
    SUCCESSFUL = 2
    STATUSES = enumerate(("Pending", "Failed", "Successful"))

    ranger = models.ForeignKey(Ranger, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    bank = models.CharField(max_length=100, null=True, blank=True)
    name = models.CharField(max_length=100, null=True, blank=True)
    payment_date = models.DateField(default=timezone.now)
    payment = models.ForeignKey(Payment, null=True, on_delete=models.SET_NULL)
    status = models.PositiveIntegerField(choices=STATUSES, default=PENDING)

    def __str__(self):
        return str(self.ranger)

    class Meta:
        ordering = ["-payment_date"]
