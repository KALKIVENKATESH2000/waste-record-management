from django.urls import path
from master.views import *
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path('', UserManagement, name='users_list'),
    path('company_details/', CompanyDetails, name='company_details'),
    path('waste_records/', CaptureWasteRecord, name='waste_records'),
    path('waste_records/list/', WasteRecordList, name='waste_records_list'),
    path('compliance_records', ComplianceCertificate, name='compliance_records'),
    path('monthly_waste/reports/', MonthlyWasteReport, name='monthly_wastwe_reports'),
    path('contrator/details', ContractorDetails, name='contrator_details'),
    path('contrator/list', ContractorList, name='contrator_list'),
     
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)