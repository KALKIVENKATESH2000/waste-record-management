from django.db import models
import calendar
from django.contrib.auth.models import AbstractUser, BaseUserManager
# from django.utils.translation import ugettext_lazy as _
from django.utils.translation import gettext_lazy as _

# Create your models here.

BRANCHES_CHOICES = (
        ('1-C', '1-C'),
        ('2-C', '2-C'),
        ('3-C', '3-C'),
    )
# SITE_NAME_CHOICES = (
#         ('Site1', 'Site1'),
#         ('Site2', 'Site2'),
#         ('Site3', 'Site3'),
#     )
LANDFILL_CHOICES = (
        ('W.D. Hall', 'W.D. Hall'),
    ) 
RECYCLEBLE_ITEM_CHOICES = (
        ('Common', 'Common'),
        ('HL1', 'HL1'),
        ('HL2', 'HL2'),
        ('K4', 'K4'),
        ('SMW', 'SMW'),
        ('SN', 'SN'),
        ('HD', 'HD'),
        ('LD Clear', 'LD Clear'),
        ('LD Mix', 'LD Mix'),
        ('LD Shrink', 'LD Shrink'),
        ('PET Brown', 'PET Brown'),
        ('PET Clear', 'PET Clear'),
        ('PET Green', 'PET Green'),
        ('Glass', 'Glass'),
    ) 
RACE_CHOICES = (
        ('Race1', 'Race1'),
        ('Race2', 'Race2'),
        ('Race3', 'Race3'),
    ) 
GENDER_CHOICES = (
        ('male', 'Male'),
        ('female', 'Female'),
        ('others', 'Others'),
    )
MONTH_CHOICES = (
        ('January', 'January'),
        ('February', 'February'),
        ('March', 'March'),
        ('April', 'April'),
        ('May', 'May'),
        ('June', 'June'),
        ('July', 'July'),
        ('August', 'August'),
        ('September', 'September'),
        ('October', 'October'),
        ('November', 'November'),
        ('December', 'December'),
)


def upload_waste_records(instance, filename):
    return 'uploads/waste_records/{filename}'.format(filename=filename)

def company_logos(instance, filename):
    return 'uploads/Company_logos/{filename}'.format(filename=filename)

class CustomUser(AbstractUser):
    member_id = models.CharField(max_length=100)
    email = models.EmailField(verbose_name="Email", null=True, unique=True, max_length=250)
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['member_id', 'username']

    def __str__(self):
        return self.first_name + " " + self.last_name
    
    
class Company(models.Model):
    name               = models.CharField(max_length=255)
    contact_number     = models.CharField(max_length=20)
    address            = models.CharField(max_length=255)
    email              = models.EmailField(max_length=50)
    person_number      = models.CharField(max_length=20)
    register_no        = models.CharField(max_length=50)
    branches           = models.CharField(max_length=150)
    vat_no             = models.CharField(max_length=50)
    company_logo       = models.FileField(upload_to=company_logos)
    createdAt          = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.name
    
class WasteRecord(models.Model):
    month                           = models.CharField(max_length=20, choices=MONTH_CHOICES)
    entry_date                      = models.DateTimeField(max_length=20)
    manifest_no                     = models.CharField(max_length=255)
    disposal_slip_no                = models.CharField(max_length=50)
    vehicle_registration            = models.CharField(max_length=20)
    bin_size                        = models.CharField(max_length=50)
    bin_GW                          = models.IntegerField()
    land_fill                       = models.CharField(max_length=50, choices=LANDFILL_CHOICES, default='W.D. Hal')
    recyclable_item                 = models.CharField(max_length=50, choices=RECYCLEBLE_ITEM_CHOICES)
    solid_waste                     = models.IntegerField()
    liquid_waste                    = models.IntegerField()
    hazardous_waste                 = models.IntegerField()
    rubble                          = models.IntegerField()
    total_waste                     = models.CharField(max_length=50)
    collection_note                 = models.FileField(upload_to=upload_waste_records)
    service_provider_certificate    = models.FileField(upload_to=upload_waste_records)
    landfill_disposal_certificate   = models.FileField(upload_to=upload_waste_records)
    lab_test_result                 = models.FileField(upload_to=upload_waste_records)
    weight_bridge_certificate       = models.FileField(upload_to=upload_waste_records)
    createdAt                       = models.DateTimeField(auto_now_add=True)
    
class Contractor(models.Model):
    site_name           = models.CharField(max_length=50)
    id_no               = models.CharField(max_length=20)
    first_name          = models.CharField(max_length=255)
    last_name           = models.CharField(max_length=50)
    contact_number      = models.CharField(max_length=20)
    gender              = models.CharField(max_length=50, choices=GENDER_CHOICES)
    employment_start    = models.DateField(max_length=20)
    employment_end      = models.DateField(max_length=20)
    race                = models.CharField(max_length=50, choices=RACE_CHOICES)
    createdAt           = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.first_name + " " + self.last_name