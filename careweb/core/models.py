from django.db import models


class Plan(models.Model):
    name = models.CharField(max_length=200)
    code = models.CharField(max_length=1, unique=True)
    client_rate = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    spouse_dependant_rate = models.DecimalField(
        max_digits=10, decimal_places=2, default=0
    )
    minor_dependant_rate = models.DecimalField(
        max_digits=10, decimal_places=2, default=0
    )
    other_dependant_rate = models.DecimalField(
        max_digits=10, decimal_places=2, default=0
    )

    def __str__(self):
        return self.name
