from django.shortcuts import render, redirect
from .models import *
from django.core.paginator import Paginator
from django.contrib import messages
import os
from datetime import datetime
from django.http import HttpResponse
from django.views.generic import View
from .utils import render_to_pdf
from django_xhtml2pdf.utils import generate_pdf
from .decorator import unauthenticated_user, admin_only, allowed_users
from django.contrib.auth.decorators import login_required
from django.contrib.auth import get_user_model
from .models import RECYCLEBLE_ITEM_CHOICES
import csv
import xlwt

# User = get_user_model()
# Create your views here.

@login_required(login_url='login')
def UserManagement(request):
    user_list = CustomUser.objects.filter(is_staff=False)
    context = {
        "user_list":user_list
    }
    return render(request, 'user-management.html', context)

def AddUser(request):
    if request.method =='POST':
        member_id = request.POST.get('member_id')
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        # username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')

        
        userObj = CustomUser.objects.create(
            member_id=member_id,
            first_name=first_name, 
            last_name=last_name, 
            username=email,
            password=password,
            email=email,
        )
        messages.success(request, 'The user “{}” was added successfully.'.format(userObj))
        return redirect('/')
    return render(request, 'user-management.html')
    
def update_user(request, user_id):
    # print(user_id)
    if request.method == 'POST':
        user = CustomUser.objects.get(id=user_id)
        user.first_name = request.POST['first_name']
        user.last_name = request.POST['last_name']
        user.is_active = request.POST['status']
        user.save()
        messages.info(request, 'The user “{}” was updated successfully.'.format(user))
        return redirect('/')

def CompanyDetails(request):
    if request.method =='POST':
        name = request.POST.get('name')
        print(name)
        contact_number = request.POST.get('contact_number')
        address = request.POST.get('address')
        email = request.POST.get('email')
        person_number = request.POST.get('person_number')
        register_no = request.POST.get('register_no')
        vat_no = request.POST.get('vat_no')
        branches = request.POST.get('branches' '')
        data = request.POST.get('data')
        print('dataaaaaaaaaa', data)
        print('&&&&&&&&&&&&',branches)
        branch_list = [tag.strip() for tag in branches.split(',') if tag.strip()]
        # branches = request.POST.getlist('branches[]')
        print('########',branch_list)

        
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
        return redirect('/company_details/')
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
        print(total_waste)
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
    return render(request, 'capture-waste-record.html', {'choices':RECYCLEBLE_ITEM_CHOICES})

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
    paginator = Paginator(wasteRecord_list, 10)
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

def WasteRecordUpdate(request, id):
    wasteRecord_Obj = WasteRecord.objects.get(id=id)
    mydate = wasteRecord_Obj.entry_date
    print(mydate)
    # entry_date = datetime.strptime(mydate, "%Y-%m-%d")
    # entry_date.strftime('%Y/%m/%d')
    # print('month',wasteRecord_Obj.month)
    if request.method =='POST':
        wasteRecord_Obj.month = request.POST['month']
        wasteRecord_Obj.entry_date = request.POST['entry_date']
        wasteRecord_Obj.manifest_no = request.POST['manifest_no']
        wasteRecord_Obj.disposal_slip_no = request.POST['disposal_slip_no']
        wasteRecord_Obj.vehicle_registration = request.POST['vehicle_registration']
        wasteRecord_Obj.bin_size = request.POST['bin_size']
        wasteRecord_Obj.bin_GW = request.POST['bin_GW']
        wasteRecord_Obj.land_fill = request.POST['land_fill']
        wasteRecord_Obj.recyclable_item = request.POST['recyclable_item']
        wasteRecord_Obj.solid_waste = request.POST['solid_waste']
        wasteRecord_Obj.liquid_waste = request.POST['liquid_waste']
        wasteRecord_Obj.hazardous_waste = request.POST['hazardous_waste']
        wasteRecord_Obj.rubble = request.POST['rubble']
        wasteRecord_Obj.total_waste = request.POST['total_waste']
        wasteRecord_Obj.collection_note = request.FILES.get('file1')
        wasteRecord_Obj.service_provider_certificate = request.FILES.get('file2')
        wasteRecord_Obj.landfill_disposal_certificate = request.FILES.get('file3')
        wasteRecord_Obj.lab_test_result = request.FILES.get('file4')
        wasteRecord_Obj.weight_bridge_certificate = request.FILES.get('file5')
        if len(request.FILES) != 0:
            if len(wasteRecord_Obj.collection_note) > 0:
                pass
                # os.remove(wasteRecord_Obj.collection_note.path)
            wasteRecord_Obj.collection_note = request.FILES['file1']
        if len(request.FILES) != 0:
            if len(wasteRecord_Obj.service_provider_certificate) > 0:
                pass
                # os.remove(wasteRecord_Obj.service_provider_certificate.path)
            wasteRecord_Obj.service_provider_certificate = request.FILES['file2']
        if len(request.FILES) != 0:
            if len(wasteRecord_Obj.landfill_disposal_certificate) > 0:
                pass
                # os.remove(wasteRecord_Obj.landfill_disposal_certificate.path)
            wasteRecord_Obj.landfill_disposal_certificate = request.FILES['file3']
        if len(request.FILES) != 0:
            if len(wasteRecord_Obj.lab_test_result) > 0:
                pass
                # os.remove(wasteRecord_Obj.lab_test_result.path)
            wasteRecord_Obj.lab_test_result = request.FILES['file4']
        if len(request.FILES) != 0:
            if len(wasteRecord_Obj.weight_bridge_certificate) > 0:
                pass
                # os.remove(wasteRecord_Obj.weight_bridge_certificate.path)
            wasteRecord_Obj.weight_bridge_certificate = request.FILES['file5']
        
        wasteRecord_Obj.save()
        messages.success(request, 'The Waste Record was changed successfully..')
        return redirect('/waste_records/list')
    else:
        context = {'wasteRecord_Obj': wasteRecord_Obj, 'mydate':mydate}
    return render(request, 'capture-waste-record.html', context)

def DelWasteRecord(request, id):
    wasteRecord_obj =  WasteRecord.objects.get(id=id)
    print(wasteRecord_obj)
    wasteRecord_obj.delete()
    messages.warning(request, 'The Waste Record “{}” was deleted successfully.'.format(wasteRecord_obj))
    return redirect('/waste_records/list')

def ComplianceCertificate(request):
    return render(request, 'compliance-certificate-download.html')



def MonthlyWasteReport(request):
    year_month = str(request.POST.get('year_month'))
    print('kkkkkkkkk',request.POST.get)
    if year_month:
        year_month = year_month.split('-')
        year = year_month[1]
        month = year_month[0]
        start_date = datetime(year=int(year), month=int(month), day=1)
        request.session['start_date'] = str(start_date)
        end_date = datetime(year=int(year), month=int(month), day=int(calendar.monthrange(int(year), int(month))[1]))
        request.session['end_date'] = str(end_date)
    else:
        messages.info(request, 'Please select month and year.')
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
    print(request.user.username)
    contractor_list = Contractor.objects.all().values()
    count = contractor_list.count()
    search_query = request.GET.get('search')
    if search_query:
        contractor_list = contractor_list.filter(
            site_name__icontains=search_query,
        )
    paginator = Paginator(contractor_list, 10)
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

def Export_ContractorList(request):
    response = HttpResponse(content_type='application/ms-excel')
    response['Content-Disposition'] = 'attachment; filename=contractors_list.xls'
    wb = xlwt.Workbook(encoding='utf-8')
    ws = wb.add_sheet('Contractors Data')
    row_num = 0

    font_style = xlwt.XFStyle()
    font_style.font.bold = True
    columns = ['ID Number', 'First Name', 'Last Name', 'Contact Number', 'Gender', 'Site Name', 'Employment Start', 'Employment End', 'Race']
    for col_num in range(len(columns)):
        ws.write(row_num, col_num, columns[col_num], font_style) 

    # Sheet body, remaining rows
    font_style = xlwt.XFStyle()

    rows = Contractor.objects.all().values_list('id_no', 'first_name', 'last_name', 'contact_number', 'gender', 'site_name', 'employment_start', 'employment_end', 'race')
    for row in rows:
        row_num += 1
        for col_num in range(len(row)):
            ws.write(row_num, col_num, str(row[col_num]), font_style)
    
    wb.save(response)

    return response
    # writer = csv.writer(response)
    # writer.writerow(['ID Number', 'First Name', 'Last Name', 'Contact Number', 'Gender', 'Site Name', 'Employment Start', 'Employment End' 'Race'])
    # contractor_fields = contractors.values_list('id_no', 'first_name', 'last_name', 'contact_number', 'gender', 'site_name', 'employment_start', 'employment_end', 'race')
    # for contractor in contractor_fields:
    #     writer.writerow(contractor)
    # return response


class GeneratePdf(View):
    def get(self, request, *args, **kwargs):
        if 'start_date' in  request.session:
            start_date = request.session.get('start_date')
            end_date = request.session.get('end_date')
            respdt = HttpResponse(content_type='application/pdf')
            filename = 'waste reports'
            context = {
                'start': datetime.strptime(start_date, '%Y-%m-%d %H:%M:%S').date(), 
                'end': datetime.strptime(end_date, '%Y-%m-%d %H:%M:%S').date(),
                'customer_name': 'Kalki',
                'order_id': 1233434,
            }
            print(context)
            # pdf = render_to_pdf('pdf/invoice.html', data)
            result = generate_pdf('pdf/invoice.html',file_object=respdt,context=context)
            result['Content-Disposition'] = 'attachment; filename="{}.pdf"'.format(filename)
            # return HttpResponse(pdf, content_type='application/pdf')
            return result
        else:
            messages.info(request, 'Please select month and year.')
        # del request.session['start_date']
        return render(request, 'monthly-waste-report.html')