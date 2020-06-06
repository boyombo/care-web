from django.contrib.auth.models import User
from django.db import models

from core.models import Plan


class SmsLog(models.Model):
    RECEIVER_CATEGORY = (
        ('A', 'All clients'),
        ('P', 'Clients under a plan'),
        ('C', 'Custom'),
    )
    STATUS = (
        ('S', "Successful"),
        ('F', "Failed")
    )
    category = models.CharField(max_length=50, choices=RECEIVER_CATEGORY)
    plan = models.ForeignKey(Plan, on_delete=models.SET_NULL, null=True, blank=True)
    recipients = models.TextField(default="", blank=True)
    message = models.TextField()
    status = models.CharField(max_length=200, choices=STATUS, default="", blank=True)
    created = models.DateTimeField(auto_now_add=True)
    sender = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return "{}".format(self.get_category_display())

    @property
    def plan_name(self):
        if self.plan:
            return self.plan.name
        return "N/A"

    @property
    def sender_name(self):
        return self.sender.username
