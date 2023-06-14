from django.db import models
import calendar

# Create your models here.

BRANCHES_CHOICES = (
        ('1-C', '1-C'),
        ('2-C', '2-C'),
        ('3-C', '3-C'),
    )
SITE_NAME_CHOICES = (
        ('Site1', 'Site1'),
        ('Site2', 'Site2'),
        ('Site3', 'Site3'),
    )
LANDFILL_CHOICES = (
        ('1', 'LandFill1'),
        ('2', 'LandFill2'),
        ('3', 'LandFill3'),
    ) 
RECYCLEBLE_ITEM_CHOICES = (
        ('1', 'item1'),
        ('2', 'item2'),
        ('3', 'item3'),
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
MONTH_CHOICES = [(str(month), calendar.month_name[month]) for month in range(1, 13)]

class Company(models.Model):
    name               = models.CharField(max_length=255)
    contact_number     = models.CharField(max_length=20)
    address            = models.CharField(max_length=255)
    email              = models.EmailField(max_length=50)
    person_number      = models.CharField(max_length=20)
    register_no        = models.CharField(max_length=50)
    branches           = models.CharField(max_length=50, choices=BRANCHES_CHOICES)
    vat_no             = models.CharField(max_length=50)
    createdAt          = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.name
    
class WasteRecord(models.Model):
    month                           = models.CharField(max_length=2, choices=MONTH_CHOICES)
    entry_date                      = models.DateField(max_length=20)
    manifest_no                     = models.CharField(max_length=255)
    disposal_slip_no                = models.CharField(max_length=50)
    vehicle_registration            = models.CharField(max_length=20)
    bin_size                        = models.CharField(max_length=50)
    bin_GW                          = models.CharField(max_length=50)
    land_fill                       = models.CharField(max_length=50, choices=LANDFILL_CHOICES)
    recyclable_item                 = models.CharField(max_length=50, choices=RECYCLEBLE_ITEM_CHOICES)
    solid_waste                     = models.CharField(max_length=50)
    liquid_waste                    = models.CharField(max_length=50)
    hazardous_waste                 = models.CharField(max_length=50)
    rubble                          = models.CharField(max_length=50)
    total_waste                     = models.CharField(max_length=50)
    collection_note                 = models.FileField(upload_to='doc/')
    service_provider_certificate    = models.FileField(upload_to='doc/')
    landfill_disposal_certificate   = models.FileField(upload_to='doc/')
    lab_test_result                 = models.FileField(upload_to='doc/')
    weight_bridge_certificate       = models.FileField(upload_to='doc/')
    createdAt                       = models.DateTimeField(auto_now_add=True)
    
class Contractor(models.Model):
    site_name           = models.CharField(max_length=50, choices=SITE_NAME_CHOICES)
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