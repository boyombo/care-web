from django.db import models

from hashid_field import HashidAutoField
from simple_history.models import HistoricalRecords

from location.models import LGA


class CareProvider(models.Model):
    id = HashidAutoField(primary_key=True)
    code_no = models.CharField(max_length=20, blank=True)
    name = models.CharField(max_length=200)
    address = models.TextField(null=True)
    phone1 = models.CharField(max_length=100, null=True, blank=True)
    phone2 = models.CharField(max_length=100, null=True, blank=True)
    lga = models.ForeignKey(LGA, null=True, on_delete=models.SET_NULL)

    history = HistoricalRecords()

    def __str__(self):
        return "{} -- {}".format(self.name, self.address)

    @property
    def lga_name(self):
        if self.lga:
            return self.lga.name
        return ""

    @property
    def lga_hash_id(self):
        if self.lga:
            return self.lga.id.hashid
        return ""
