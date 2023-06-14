from django.contrib import admin
from .models import *
# Register your models here.

class CompanyAdmin(admin.ModelAdmin):
    list_display = [f.name for f in Company._meta.get_fields()]
admin.site.register(Company, CompanyAdmin)


class WasteRecordAdmin(admin.ModelAdmin):
    list_display = [f.name for f in WasteRecord._meta.get_fields()]
admin.site.register(WasteRecord, WasteRecordAdmin)

class ContractorAdmin(admin.ModelAdmin):
    list_display = [f.name for f in Contractor._meta.get_fields()]
admin.site.register(Contractor, ContractorAdmin)