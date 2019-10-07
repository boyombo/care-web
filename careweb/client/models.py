from django.db import models


class CareProvider(models.Model):
    code_no = models.CharField(max_length=20)
    name = models.CharField(max_length=200)

    def __str__(self):
        return self.name


class Ranger(models.Model):
    first_name = models.CharField(max_length=200)
    last_name = models.CharField(max_length=200)
    phone = models.CharField(max_length=50)

    def __str__(self):
        return '{} {}'.format(self.first_name, self.last_name)


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

    surname = models.CharField(max_length=100)
    first_name = models.CharField(max_length=100)
    middle_name = models.CharField(max_length=100, blank=True)
    dob = models.DateField(null=True, blank=True)
    designation = models.PositiveIntegerField(choices=DESIGNATIONS)
    pcp = models.ForeignKey(CareProvider, null=True, on_delete=models.SET_NULL)

    def __str__(self):
        return self.surname


class Client(models.Model):
    FEMALE = 0
    MALE = 1
    SEXES = enumerate(('Female', 'Male'))

    SINGLE = 0
    MARRIED = 1
    DIVORCED = 2
    MARITAL_STATUSES = enumerate(('Single', 'Married', 'Divorced'))

    LASHMA = 0
    LASHMA_QUALITY_LIFE = 1
    PACKAGE_OPTIONS = enumerate(('LASHMA', 'LASHMA QUALITY LIFE'))

    WEEKLY = 0
    MONTHLY = 1
    QUARTERLY = 2
    ANNUALLY = 3
    PAYMENT_OPTIONS = enumerate(('Weekly', 'Monthly', 'Quarterly', 'Annually'))

    TRANSFER = 0
    EWALLET = 1
    CHEQUE = 2
    BANK_DEPOSIT = 3
    PAYMENT_INSTRUMENTS = enumerate(
        ('Transfer', 'E-Wallet', 'Cheque', 'Bank Deposit'))

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
    pcp = models.ForeignKey(CareProvider, null=True, on_delete=models.SET_NULL)
    ranger = models.ForeignKey(Ranger, null=True, on_delete=models.SET_NULL)
    home_address = models.TextField(blank=True)
    occupation = models.CharField(max_length=200, blank=True)
    company = models.CharField(max_length=200, blank=True)
    office_address = models.TextField(blank=True)
    hmo = models.ForeignKey(HMO, null=True, on_delete=models.SET_NULL)
    informal_sector_group = models.CharField(max_length=200, null=True)
    package_option = models.PositiveIntegerField(
        choices=PACKAGE_OPTIONS, null=True)
    payment_option = models.PositiveIntegerField(
        choices=PAYMENT_OPTIONS, null=True)
    payment_instrument = models.PositiveIntegerField(
        choices=PAYMENT_INSTRUMENTS, null=True)
    dependants = models.ManyToManyField(Dependant, blank=True)

    def __str__(self):
        return self.surname
