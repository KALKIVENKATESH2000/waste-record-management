from django.contrib import admin
from .models import *
from django.contrib.auth.admin import UserAdmin

# Register your models here.

class CustomUserAdmin(admin.ModelAdmin):
    # Specify the list of fields to be displayed in the admin list view
    list_display = ['id', 'company', 'username', 'email', 'member_id', 'is_staff']
admin.site.register(CustomUser, CustomUserAdmin)

class CompanyAdmin(admin.ModelAdmin):
    # list_display = [f.name for f in Company._meta.get_fields()]
    list_display = ['id', 'name', 'contact_number', 'address', 'email', 'person_number', 'register_no', 'branches', 'vat_no', 'company_logo']
admin.site.register(Company, CompanyAdmin)


class WasteRecordAdmin(admin.ModelAdmin):
    # list_display = ['id', 'user']
    list_display = [f.name for f in WasteRecord._meta.get_fields()]
admin.site.register(WasteRecord, WasteRecordAdmin)

class ContractorAdmin(admin.ModelAdmin):
    list_display = [f.name for f in Contractor._meta.get_fields()]
admin.site.register(Contractor, ContractorAdmin)

class DocumentAdmin(admin.ModelAdmin):
    list_display = [f.name for f in Document._meta.get_fields()]
admin.site.register(Document, DocumentAdmin)