from django.db import models
from django.utils import timezone

from location.models import LGA
from provider.models import CareProvider
from ranger.models import Ranger


#class LGA(models.Model):
#    name = models.CharField(max_length=100)

#    def __str__(self):
#        return self.name


#class Location(models.Model):
#    name = models.CharField(max_length=100)
#    lga = models.ForeignKey(LGA, on_delete=models.CASCADE)

#    def __str__(self):
#        return self.name


#class CareProvider(models.Model):
#    code_no = models.CharField(max_length=20, blank=True)
#    name = models.CharField(max_length=200)
#    address = models.TextField(null=True)
#    phone1 = models.CharField(max_length=100, null=True, blank=True)
#    phone2 = models.CharField(max_length=100, null=True, blank=True)
#    lga = models.ForeignKey(LGA, null=True, on_delete=models.SET_NULL)

#    def __str__(self):
#        return self.name


#class Ranger(models.Model):
#    first_name = models.CharField(max_length=200)
#    last_name = models.CharField(max_length=200)
#    phone = models.CharField(max_length=50)
#    lga = models.ForeignKey(LGA, null=True, on_delete=models.SET_NULL)

#    def __str__(self):
#        return '{} {}'.format(self.first_name, self.last_name)


class HMO(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Dependant(models.Model):
    SPOUSE = 0
    DAUGHTER = 1
    SON = 2
    OTHERS = 3
    DESIGNATIONS = enumerate(('Spouse', 'Daughter', 'Son', 'Others'))

    primary = models.ForeignKey('Client', null=True, on_delete=models.SET_NULL)
    surname = models.CharField(max_length=100)
    first_name = models.CharField(max_length=100)
    middle_name = models.CharField(max_length=100, blank=True)
    dob = models.DateField(null=True, blank=True)
    designation = models.PositiveIntegerField(choices=DESIGNATIONS)
    pcp = models.ForeignKey(CareProvider, null=True, on_delete=models.SET_NULL)

    def __str__(self):
        return self.surname


class Client(models.Model):
    FEMALE = 'F'
    MALE = 'M'
    SEXES = (('F', 'Female'), ('M', 'Male'))
    #SEXES = enumerate(('Female', 'Male'))

    SINGLE = 'S'
    MARRIED = 'M'
    DIVORCED = 'D'
    MARITAL_STATUSES = (('S', 'Single'), ('M', 'Married'), ('D', 'Divorced'))

    LASHMA = 'L'
    LASHMA_QUALITY_LIFE = 'Q'
    PACKAGE_OPTIONS = (('L', 'LASHMA'), ('Q', 'LASHMA QUALITY LIFE'))

    WEEKLY = 'W'
    MONTHLY = 'M'
    QUARTERLY = 'Q'
    ANNUALLY = 'A'
    PAYMENT_OPTIONS = (
        ('W', 'Weekly'),
        ('M', 'Monthly'),
        ('Q', 'Quarterly'),
        ('A', 'Annually')
    )

    TRANSFER = 'T'
    EWALLET = 'E'
    CHEQUE = 'C'
    BANK_DEPOSIT = 'B'
    PAYMENT_INSTRUMENTS = (
        ('T', 'Transfer'),
        ('E', 'E-Wallet'),
        ('C', 'Cheque'),
        ('B', 'Bank Deposit')
    )

    surname = models.CharField(max_length=100)
    first_name = models.CharField(max_length=100)
    middle_name = models.CharField(max_length=100, blank=True)
    dob = models.DateField(null=True, blank=True)
    sex = models.CharField(max_length=10, choices=SEXES)
    #sex = models.PositiveIntegerField(choices=SEXES)
    marital_status = models.CharField(max_length=10, choices=MARITAL_STATUSES)
    national_id_card_no = models.CharField(max_length=50, blank=True)
    drivers_licence_no = models.CharField(max_length=50, blank=True)
    lashma_no = models.CharField(max_length=50, blank=True)
    lashma_quality_life_no = models.CharField(max_length=50, blank=True)
    lagos_resident_no = models.CharField(max_length=50, blank=True)
    phone_no = models.CharField(max_length=50, blank=True)
    whatsapp_no = models.CharField(max_length=50, blank=True)
    email = models.CharField(max_length=50, blank=True)
    pcp = models.ForeignKey(
        CareProvider, null=True, blank=True, on_delete=models.SET_NULL)
    ranger = models.ForeignKey(Ranger, null=True, on_delete=models.SET_NULL)
    home_address = models.TextField(blank=True)
    occupation = models.CharField(max_length=200, blank=True)
    company = models.CharField(max_length=200, blank=True)
    office_address = models.TextField(blank=True)
    hmo = models.ForeignKey(
        HMO, null=True, blank=True, on_delete=models.SET_NULL)
    informal_sector_group = models.CharField(
        max_length=200, blank=True, null=True)
    package_option = models.CharField(
        max_length=50, choices=PACKAGE_OPTIONS, null=True)
    payment_option = models.CharField(
        max_length=50, choices=PAYMENT_OPTIONS, null=True)
    payment_instrument = models.CharField(
        max_length=20, choices=PAYMENT_INSTRUMENTS, null=True)
    registration_date = models.DateField(default=timezone.now)
    #dependants = models.ManyToManyField(Dependant, blank=True)

    def __str__(self):
        return self.surname
