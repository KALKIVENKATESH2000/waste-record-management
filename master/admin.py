from django.contrib import admin
from .models import *
from django.contrib.auth.admin import UserAdmin

# Register your models here.

class CustomUserAdmin(UserAdmin):
    # Specify the list of fields to be displayed in the admin list view
    list_display = ['id','username', 'email', 'member_id', 'is_staff']
admin.site.register(CustomUser, CustomUserAdmin)

class CompanyAdmin(admin.ModelAdmin):
    list_display = [f.name for f in Company._meta.get_fields()]
admin.site.register(Company, CompanyAdmin)


class WasteRecordAdmin(admin.ModelAdmin):
    list_display = [f.name for f in WasteRecord._meta.get_fields()]
admin.site.register(WasteRecord, WasteRecordAdmin)

class ContractorAdmin(admin.ModelAdmin):
    list_display = [f.name for f in Contractor._meta.get_fields()]
admin.site.register(Contractor, ContractorAdmin)