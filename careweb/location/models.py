from django.db import models

from hashid_field import HashidAutoField
from simple_history.models import HistoricalRecords


class LGA(models.Model):
    id = HashidAutoField(primary_key=True)
    name = models.CharField(max_length=100)

    history = HistoricalRecords()

    def __str__(self):
        return self.name
