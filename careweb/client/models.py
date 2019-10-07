from django.db import models


class Client(models.Model):
    FEMALE = 0
    MALE = 1
    SEXES = enumerate(('Female', 'Male'))

    SINGLE = 0
    MARRIED = 1
    DIVORCED = 2
    MARITAL_STATUSES = enumerate(('Single', 'Married', 'Divorced'))

    surname = models.CharField(max_length=100)
    first_name = models.CharField(max_length=100)
    middle_name = models.CharField(max_length=100, blank=True)
    dob = models.DateField(null=True, blank=True)
    sex = models.PositiveIntegerField(choices=SEXES)
    marital_status = models.PositiveIntegerField(choices=MARITAL_STATUSES)
    national_id_card_no = models.CharField(max_length=50, blank=True)
    drivers_licence_no = models.CharField(max_length=50, blank=True)
    lashma_no = models.CharField(max_length=50, blank=True)
    lashma_quality_life_no = models.CharField(max_length=50, blank=True)
    lagos_resident_no = models.CharField(max_length=50, blank=True)
    phone_no = models.CharField(max_length=50, blank=True)
    whatsapp_no = models.CharField(max_length=50, blank=True)
    email = models.CharField(max_length=50, blank=True)
