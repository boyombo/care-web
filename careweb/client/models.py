from django.contrib.auth.models import User
from django.db import models
from django.utils import timezone
from django.urls import reverse

# from location.models import LGA
from provider.models import CareProvider
from ranger.models import Ranger


class Association(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class ClientAssociation(models.Model):
    client = models.ForeignKey('Client', on_delete=models.CASCADE)
    association = models.ForeignKey('Association', on_delete=models.CASCADE)

    class Meta:
        verbose_name = 'Associations'

    def __str__(self):
        return str(self.association)


class HMO(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


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


class Client(models.Model):
    FEMALE = 'F'
    MALE = 'M'
    SEXES = (('F', 'Female'), ('M', 'Male'))
    # SEXES = enumerate(('Female', 'Male'))

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
    CARD = 'D'
    EWALLET = 'E'
    CHEQUE = 'C'
    BANK_DEPOSIT = 'B'
    PAYMENT_INSTRUMENTS = (
        ('T', 'Transfer'),
        ('D', 'Debit Card'),
        ('E', 'E-Wallet'),
        ('C', 'Cheque'),
        ('B', 'Bank Deposit')
    )

    user = models.ForeignKey(
        User, on_delete=models.CASCADE, null=True, blank=True)
    surname = models.CharField(max_length=100)
    first_name = models.CharField(max_length=100)
    middle_name = models.CharField(max_length=100, blank=True)
    dob = models.DateField('Date of Birth', null=True, blank=True)
    sex = models.CharField('Gender', max_length=10, choices=SEXES, null=True)
    #sex = models.PositiveIntegerField(choices=SEXES)
    marital_status = models.CharField(
        max_length=10, choices=MARITAL_STATUSES, null=True)
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
    # informal_sector_group = models.CharField(
    #    max_length=200, blank=True, null=True)
    #associations = models.ManyToManyField('Association', related_name='client_associations')
    package_option = models.CharField(
        max_length=50, choices=PACKAGE_OPTIONS, null=True)
    payment_option = models.CharField(
        max_length=50, choices=PAYMENT_OPTIONS, null=True)
    payment_instrument = models.CharField(
        max_length=20, choices=PAYMENT_INSTRUMENTS, null=True)
    registration_date = models.DateField(default=timezone.now)
    photo = models.ImageField(upload_to='clientphoto', null=True, blank=True)
    #dependants = models.ManyToManyField(Dependant, blank=True)

    def __str__(self):
        return self.surname

    def get_absolute_url(self):
        return reverse('profile', kwargs={'pk': self.pk})
