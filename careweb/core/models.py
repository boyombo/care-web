from django.db import models
from simple_history.models import HistoricalRecords


class Plan(models.Model):
    name = models.CharField(max_length=200)
    code = models.CharField(max_length=1, unique=True)
    has_extra = models.BooleanField(default=False)
    family_inclusive = models.BooleanField(default=True)
    size = models.PositiveIntegerField(null=True)

    history = HistoricalRecords()
    # client_rate = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    # spouse_dependant_rate = models.DecimalField(
    #    max_digits=10, decimal_places=2, default=0
    # )
    # minor_dependant_rate = models.DecimalField(
    #    max_digits=10, decimal_places=2, default=0
    # )
    # other_dependant_rate = models.DecimalField(
    #    max_digits=10, decimal_places=2, default=0
    # )

    def __str__(self):
        return self.name


class PlanRate(models.Model):
    DAILY = "D"
    WEEKLY = "W"
    MONTHLY = "M"
    ANNUALLY = "A"

    PAYMENT_CYCLES = (
        ("D", "Daily"),
        ("W", "Weekly"),
        ("M", "Monthly"),
        ("A", "Annually"),
    )

    plan = models.ForeignKey(Plan, on_delete=models.CASCADE)
    payment_cycle = models.CharField(choices=PAYMENT_CYCLES, max_length=2)
    rate = models.PositiveIntegerField()
    extra_rate = models.PositiveIntegerField(null=True, blank=True)

    history = HistoricalRecords()

    def __str__(self):
        return str(self.plan)

    @property
    def has_extra(self):
        return self.plan.has_extra


class SmsLog(models.Model):
    recipient = models.TextField(default="", blank=True)
    message = models.TextField()
    status = models.CharField(max_length=200, default="", blank=True)
