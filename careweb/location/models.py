from django.db import models

from hashid_field import HashidAutoField


class LGA(models.Model):
    id = HashidAutoField(primary_key=True)
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name
