from django.db import models

from location.models import LGA


class CareProvider(models.Model):
    code_no = models.CharField(max_length=20, blank=True)
    name = models.CharField(max_length=200)
    address = models.TextField(null=True)
    phone1 = models.CharField(max_length=100, null=True, blank=True)
    phone2 = models.CharField(max_length=100, null=True, blank=True)
    lga = models.ForeignKey(LGA, null=True, on_delete=models.SET_NULL)

    def __str__(self):
        return self.name
