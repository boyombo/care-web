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
    email = models.EmailField(null=True, blank=True)  # Added email field for PCP auth
    uses_default_password = models.BooleanField(default=False)
    created = models.DateTimeField(auto_now_add=True)

    history = HistoricalRecords()

    def __str__(self):
        return "{} -- {}".format(self.name, self.address)

    class Meta:
        permissions = (
            ('is_provider', 'Care Provider'),
        )

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


class ProviderComment(models.Model):
    id = HashidAutoField(primary_key=True)
    provider = models.ForeignKey(CareProvider, on_delete=models.CASCADE)
    # Client would be the enrollee attended to or the principal if it was a dependant
    client = models.ForeignKey('client.Client', on_delete=models.CASCADE)
    dependant = models.ForeignKey('client.Dependant', on_delete=models.CASCADE, null=True, blank=True)
    doctor = models.CharField(max_length=200)
    comment = models.TextField()
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)

    history = HistoricalRecords()

    def __str__(self):
        return "{} -- {}".format(self.provider, self.client)
