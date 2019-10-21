from django.db import models
from django.contrib.auth.models import User

from location.models import LGA


class Ranger(models.Model):
    user = models.ForeignKey(
        User, null=True, blank=True, on_delete=models.SET_NULL)
    first_name = models.CharField(max_length=200)
    last_name = models.CharField(max_length=200)
    phone = models.CharField(max_length=50)
    lga = models.ForeignKey(LGA, null=True, on_delete=models.SET_NULL)
    balance = models.DecimalField(max_digits=10, decimal_places=2, default=0)

    def __str__(self):
        return '{} {}'.format(self.first_name, self.last_name)
