from django.shortcuts import render, redirect
from .models import *
from django.core.paginator import Paginator
from django.contrib import messages

# Create your views here.


def UserManagement(request):
    return render(request, 'user-management.html')

def CompanyDetails(request):
    if request.method =='POST':
        name = request.POST.get('name')
        print(name)
        contact_number = request.POST.get('contact_number')
        address = request.POST.get('address')
        email = request.POST.get('email')
        person_number = request.POST.get('person_number')
        register_no = request.POST.get('register_no')
        branches = request.POST.get('branches')
        vat_no = request.POST.get('vat_no')

        company_obj = Company.objects.create(
            name=name,
            contact_number=contact_number, 
            address=address, 
            email=email,
            person_number=person_number,
            register_no=register_no,
            branches=branches,
            vat_no=vat_no
        )
        messages.success(request, 'The Companey “{}” was added successfully.'.format(company_obj))
        return redirect('/company_details')
    return render(request, 'company-details.html')

def CaptureWasteRecord(request):
    if request.method =='POST':
        month = request.POST.get('month')
        entry_date = request.POST.get('entry_date')
        manifest_no = request.POST.get('manifest_no')
        disposal_slip_no = request.POST.get('disposal_slip_no')
        vehicle_registration = request.POST.get('vehicle_registration')
        bin_size = request.POST.get('bin_size')
        bin_GW = request.POST.get('bin_GW')
        land_fill = request.POST.get('land_fill')
        recyclable_item = request.POST.get('recyclable_item')
        solid_waste = request.POST.get('solid_waste')
        liquid_waste = request.POST.get('liquid_waste')
        hazardous_waste = request.POST.get('hazardous_waste')
        rubble = request.POST.get('rubble')
        total_waste = request.POST.get('total_waste')
        collection_note = request.FILES.get('file1')
        service_provider_certificate = request.FILES.get('file2')
        landfill_disposal_certificate = request.FILES.get('file3')
        lab_test_result = request.FILES.get('file4')
        weight_bridge_certificate = request.FILES.get('file5')

        cwr_obj = WasteRecord.objects.create(
            month=month,
            entry_date=entry_date, 
            manifest_no=manifest_no, 
            disposal_slip_no=disposal_slip_no,
            vehicle_registration=vehicle_registration,
            bin_size=bin_size,
            bin_GW=bin_GW,
            land_fill=land_fill,
            recyclable_item=recyclable_item,
            solid_waste=solid_waste,
            liquid_waste=liquid_waste,
            hazardous_waste=hazardous_waste,
            rubble=rubble,
            total_waste=total_waste,
            collection_note=collection_note,
            service_provider_certificate=service_provider_certificate,
            landfill_disposal_certificate=landfill_disposal_certificate,
            lab_test_result=lab_test_result,
            weight_bridge_certificate=weight_bridge_certificate,
        )
        messages.success(request, 'The capture waste record was added successfully.')
        return redirect('/waste_records')
    return render(request, 'capture-waste-record.html')

def WasteRecordList(request):
    wasteRecord_list = WasteRecord.objects.all()
    # print(wasteRecord_list)
    search_query = request.GET.get('search')
    if search_query:
        wasteRecord_list = wasteRecord_list.filter(
            disposal_slip_no__icontains=search_query,
            # manifest_no__icontains=search_query,
            # land_fill__icontains=search_query,
            # entry_date__icontains=search_query,
        )
    paginator = Paginator(wasteRecord_list, 5)  # Show 10 items per page
    page = request.GET.get('page')
    
    try:
        wasteRecord_list = paginator.get_page(page)
    except PageNotAnInteger:
        wasteRecord_list = paginator.get_page(1)
    except EmptyPage:
        wasteRecord_list = paginator.get_page(paginator.num_pages)
        
    context = {
        "wasteRecord_Obj":wasteRecord_list, 
        'search_query': search_query,
    }
    return render(request, 'waste-record-list.html', context)

def ComplianceCertificate(request):
    return render(request, 'compliance-certificate-download.html')

def MonthlyWasteReport(request):
    return render(request, 'monthly-waste-report.html')

def ContractorDetails(request):
    if request.method =='POST':
        site_name = request.POST.get('site_name')
        id_no = request.POST.get('id_no')
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        contact_number = request.POST.get('contact_number')
        gender = request.POST.get('gender')
        employment_start = request.POST.get('employment_start')
        employment_end = request.POST.get('employment_end')
        race = request.POST.get('race')

        contractor_obj = Contractor.objects.create(
            site_name=site_name,
            id_no=id_no, 
            first_name=first_name, 
            last_name=last_name,
            contact_number=contact_number,
            gender=gender,
            employment_start=employment_start,
            employment_end=employment_end,
            race=race,
        )
        messages.success(request, 'The Contractor “{}” was added successfully.'.format(contractor_obj))
        return redirect('/contrator/details')
    return render(request, 'contractor-details.html')

def ContractorList(request):
    contractor_list = Contractor.objects.all().values()
    count = contractor_list.count()
    search_query = request.GET.get('search')
    if search_query:
        contractor_list = contractor_list.filter(
            site_name__icontains=search_query,
        )
    paginator = Paginator(contractor_list, 5)
    page = request.GET.get('page')
    
    try:
        contractor_list = paginator.get_page(page)
    except PageNotAnInteger:
        contractor_list = paginator.get_page(1)
    except EmptyPage:
        contractor_list = paginator.get_page(paginator.num_pages)
    context = {"contractor_Obj":contractor_list, 
               "search_query":search_query,
               "count": count
    }
    return render(request, 'contractor-list.html', context)