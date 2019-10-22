from django.contrib.auth.models import User
from django.db import models
from django.utils import timezone

#from location.models import LGA
from provider.models import CareProvider
from ranger.models import Ranger
from django.contrib.auth.models import User


class Association(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class HMO(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Client(models.Model):
    # FEMALE = 'F'
    # MALE = 'M'
    SEX = (
        ('F', 'Female'), 
        ('M', 'Male')
        )

    MARITAL_STATUSES = (
        ('S', 'Single'), 
        ('M', 'Married'), 
        ('D', 'Divorced')
        )

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    ranger = models.ForeignKey(Ranger, null=True, on_delete=models.SET_NULL)
    middle_name = models.CharField(max_length=100, blank=True)
    dob = models.DateField(null=True, blank=True)
    sex = models.CharField(max_length=10, choices=SEX)
    marital_status = models.CharField(max_length=10, choices=MARITAL_STATUSES)
    national_id_card_no = models.CharField(max_length=50, blank=True)
    drivers_licence_no = models.CharField(max_length=50, blank=True)
    lagos_resident_no = models.CharField(max_length=50, blank=True)
    phone_no = models.CharField(max_length=11, blank=True)
    whatsapp_no = models.CharField(max_length=11, blank=True)
    home_address = models.TextField(blank=True)
    occupation = models.CharField(max_length=200, blank=True)
    company = models.CharField(max_length=200, blank=True)
    office_address = models.TextField(blank=True)
    associations = models.ManyToManyField('Association')
    registration_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.user


class Insurance(models.Model):

    PACKAGE_OPTION = (
        ('L', 'LASHMA'), 
        ('Q', 'LASHMA QUALITY LIFE')
        )

    PAYMENT_OPTION = (
        ('W', 'Weekly'),
        ('M', 'Monthly'),
        ('Q', 'Quarterly'),
        ('A', 'Annually')
    )

    PAYMENT_INSTRUMENT = (
        ('T', 'Transfer'),
        ('E', 'E-Wallet'),
        ('C', 'Cheque'),
        ('B', 'Bank Deposit')
    )

    user = models.ForeignKey(
        User, null=True, blank=True, on_delete=models.SET_NULL)
    client = models.ForeignKey(Client, on_delete=models.CASCADE, related_name='client')
    hmo = models.ForeignKey(HMO, on_delete=models.CASCADE, related_name='hmo')
    package_option = models.CharField(max_length=50, choices=PACKAGE_OPTION)
    payment_option = models.CharField(max_length=50, choices=PAYMENT_OPTION)
    payment_instrument = models.CharField(max_length=50, 
                                          choices=PAYMENT_INSTRUMENT, null=True)
    pcp = models.ForeignKey(CareProvider, null=True, blank=True, 
                            on_delete=models.SET_NULL)
    lashma_no = models.CharField(max_length=50, blank=True)
    lashma_quality_life_no = models.CharField(max_length=50, blank=True)


class Dependant(models.Model):

    SPOUSE = 0
    DAUGHTER = 1
    SON = 2
    OTHERS = 3
    RELATIONSHIPS = enumerate(('Spouse', 'Daughter', 'Son', 'Others'))

    primary = models.ForeignKey('Client', null=True, on_delete=models.SET_NULL)
    surname = models.CharField(max_length=100)
    first_name = models.CharField(max_length=100)
    middle_name = models.CharField(max_length=100, blank=True)
    dob = models.DateField(null=True, blank=True)
    relationship = models.PositiveIntegerField(choices=RELATIONSHIPS)
    pcp = models.ForeignKey(CareProvider, null=True, on_delete=models.SET_NULL)

    def __str__(self):
        return self.surname