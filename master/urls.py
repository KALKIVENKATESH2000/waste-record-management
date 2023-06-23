from django.urls import path
from master.views import *
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path('', UserManagement, name='users_list'),
    path('add_user/', AddUser, name='add_user'),
    path('update_user/<int:user_id>/', update_user, name='update_user'),

    path('company_details/', CompanyDetails, name='company_details'),
    path('waste_records/', CaptureWasteRecord, name='waste_records'),
    path('waste_record/<int:id>', WasteRecordUpdate ,name='waste_record_update'),
    path('waste_records/list/', WasteRecordList, name='waste_records_list'),
    path('waste_record/<int:id>/delete', DelWasteRecord, name='delete_waste_record'),
    path('compliance_records', ComplianceCertificate, name='compliance_records'),
    path('monthly_waste/reports/', MonthlyWasteReport, name='monthly_wastwe_reports'),
    path('contrator/details', ContractorDetails, name='contrator_details'),
    path('contrator/list', ContractorList, name='contrator_list'),
    path('contrator/list/export_csv', Export_ContractorList, name='export_contractors_list'),
    path('download/', GeneratePdf.as_view(), name='download_reports')
     
    
     
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)