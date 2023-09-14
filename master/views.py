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
from django.db.models import Sum
from django.db.models import Count
from django.core.mail import send_mail
from django.contrib.auth.hashers import make_password





# User = get_user_model()
# Create your views here.
@login_required(login_url='login')
def UserManagement(request):
    if request.user.is_superuser:
        user_list = CustomUser.objects.filter(is_staff=False)
        user_count = user_list.count()
        companies = Company.objects.all()
        search_query = request.GET.get('search')
        if search_query:
            user_list = user_list.filter(
                first_name__icontains=search_query,
            )
        paginator = Paginator(user_list, 10)
        page = request.GET.get('page')
        
        try:
            user_list = paginator.get_page(page)
        except PageNotAnInteger:
            user_list = paginator.get_page(1)
        except EmptyPage:
            user_list = paginator.get_page(paginator.num_pages)
        context = {
            "user_list" : user_list,
            "user_count" : user_count,
            "search_query": search_query,
            'companies':companies,
        }
        return render(request, 'user-management.html', context)
    else:
        return redirect('company_details/')

def AddUser(request):
    if request.method =='POST':
        company = request.POST.get('companies')
        
        member_id = request.POST.get('member_id')
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        email = request.POST.get('email')
        password = request.POST.get('password')

        userObj = CustomUser.objects.create_user(
            member_id=member_id,
            first_name=first_name, 
            last_name=last_name, 
            username=email,
            company_id=company,
            password=password,
            email=email,
        )
        
        # subject = 'Your Kaysim-WRS Account Information'
        # message = f'Username: {email}\n\nPassword: {password}'
        # from_email = 'no-reply@vibhotech.com'
        # recipient_list = [email]

        # send_mail(subject, message, from_email, recipient_list, fail_silently=False)
        
        messages.success(request, 'The user “{}” was added successfully.'.format(userObj))
        return redirect('/')
    return render(request, 'user-management.html')

def update_user(request, user_id):
    if request.method == 'POST':
        user = CustomUser.objects.get(id=user_id)
        user.first_name = request.POST['first_name']
        user.last_name = request.POST['last_name']
        # user.password = make_password(request.POST['password'])
        user.is_active = request.POST['status']
        
        new_password = request.POST.get('password')
        if new_password:
            user.password = make_password(new_password)
        user.save()
        messages.info(request, 'The user “{}” was updated successfully.'.format(user))
        return redirect('/')

@login_required(login_url='login')
def CompanyDetails(request):
    if request.user.is_superuser:
        if request.method =='POST':
            name = request.POST.get('name')
            contact_number = request.POST.get('contact_number')
            address = request.POST.get('address')
            email = request.POST.get('email')
            person_number = request.POST.get('person_number')
            register_no = request.POST.get('register_no')
            vat_no = request.POST.get('vat_no')
            company_logo = request.FILES.get('logo')
            branches = request.POST.get('branches' '')
            data = request.POST.get('data')
            branch_list = [tag.strip() for tag in branches.split(',') if tag.strip()]
            # branches = request.POST.getlist('branches[]')
            
            company_obj = Company.objects.create(
                name=name,
                contact_number=contact_number, 
                address=address, 
                email=email,
                person_number=person_number,
                register_no=register_no,
                branches=branches,
                vat_no=vat_no,
                company_logo=company_logo,
            )
            messages.success(request, 'The Companey “{}” was added successfully.'.format(company_obj))
            return redirect('/company_details/')
        return render(request, 'company-details.html')
    else:
        company = request.user.company
        company_details = Company.objects.get(name=company)
        if request.method =='POST':
            company_details.branches = request.POST.get('branches' '')
            company_details.save()
            messages.success(request, 'The branches “{}” was updated.'.format(company_details.branches))
            return redirect('/company_details/')
        return render(request, 'company-details.html', {'company':company_details})
        

def CaptureWasteRecord(request):
    branches = []
    if request.user.is_superuser:
        branches_list = list(set(Company.objects.values_list('branches', flat=True)))
        companies_list = Company.objects.all()
    else:
        company = request.user.company
        branches_list = Company.objects.filter(name=company).values_list('branches', flat=True)
    joined_string = ','.join(branches_list)
    result = [value.strip() for value in joined_string.split(',')]
    unique_values = list(set(result))
    for branch in unique_values:
        branches.append(branch)
    if request.method =='POST':
        month = request.POST.get('month')
        branch = request.POST.get('branch')
        company = request.POST.get('company')
        print(company)
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
            user_id=request.user.id,
            month=month,
            branch=branch,
            company_id=company,
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
    return render(request, 'capture-waste-record.html', {'choices':RECYCLEBLE_ITEM_CHOICES, 'branches':branches, 'companies':companies_list})

def WasteRecordList(request):
    if request.user.is_superuser:
        wasteRecord_list = WasteRecord.objects.all()
    else:
        wasteRecord_list = WasteRecord.objects.filter(user=request.user.id)
        
    search_query = request.GET.get('search')
    if search_query:
        wasteRecord_list = wasteRecord_list.filter(disposal_slip_no__icontains=search_query,)
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
            
        file1 = request.FILES.get('file1')
        if file1:
            if wasteRecord_Obj.collection_note:
                wasteRecord_Obj.collection_note.delete()
            wasteRecord_Obj.collection_note = file1
            
        file2 = request.FILES.get('file2')
        if file2:
            if wasteRecord_Obj.service_provider_certificate:
                wasteRecord_Obj.service_provider_certificate.delete()
            wasteRecord_Obj.service_provider_certificate = file2
            
        file3 = request.FILES.get('file3')
        if file3:
            if wasteRecord_Obj.landfill_disposal_certificate:
                wasteRecord_Obj.landfill_disposal_certificate.delete()
            wasteRecord_Obj.landfill_disposal_certificate = file3
            
        file4 = request.FILES.get('file4')
        if file4:
            if wasteRecord_Obj.lab_test_result:
                wasteRecord_Obj.lab_test_result.delete()
            wasteRecord_Obj.lab_test_result = file4
            
        file5 = request.FILES.get('file5')
        if file5:
            if wasteRecord_Obj.weight_bridge_certificate:
                wasteRecord_Obj.weight_bridge_certificate.delete()
            wasteRecord_Obj.weight_bridge_certificate = file5
        
        wasteRecord_Obj.save()
        messages.success(request, 'The Waste Record was changed successfully..')
        return redirect('/waste_records/list')
    else:
        context = {'wasteRecord_Obj': wasteRecord_Obj, 'mydate':mydate, 'choices':RECYCLEBLE_ITEM_CHOICES}
    return render(request, 'waste-record-update.html', context)

def DelWasteRecord(request, id):
    wasteRecord_obj =  WasteRecord.objects.get(id=id)
    wasteRecord_obj.delete()
    messages.warning(request, 'The Waste Record “{}” was deleted successfully.'.format(wasteRecord_obj))
    return redirect('/waste_records/list')

def ComplianceCertificate(request):
    documents = Document.objects.all()
    return render(request, 'compliance-certificate-download.html', {'documents':documents})


def MonthlyWasteReport(request):
    companies_list = Company.objects.all()
    year_month = str(request.POST.get('year_month'))
    companyId = request.POST.get('company')
    conpany = request.user.company
    print('#########',companyId, conpany)
    # print(request.user.id)
    if request.method == 'POST':
        if year_month:
            year_month = year_month.split('-')
            month = year_month[0]
            year = year_month[1]
            start_date = datetime(year=int(year), month=int(month), day=1)
            request.session['start_date'] = str(start_date)
            end_date = datetime(year=int(year), month=int(month), day=int(calendar.monthrange(int(year), int(month))[1]))
            request.session['end_date'] = str(end_date)
            request.session['companyId'] = companyId
            return redirect('/waste_reports/')
        else:
            messages.info(request, 'select year and month')
    else:
        pass
    return render(request, 'monthly-waste-report.html', {'companies_list':companies_list})



def ContractorDetails(request):
    sites = []
    site_list = list(set(Company.objects.values_list('branches', flat=True)))
    joined_string = ','.join(site_list)
    result = [value.strip() for value in joined_string.split(',')]
    unique_values = list(set(result))
    for site in unique_values:
        sites.append(site)
        
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
    context = {'sites':sites}
    return render(request, 'contractor-details.html', context)

def ContractorList(request):
    sites = []
    company = request.user.company
    print('%%%%%%%%%%%%%%5',company)
    site_list = Company.objects.filter(name=company).values_list('branches', flat=True)
    # site_list = list(set(Company.objects.values_list('branches', flat=True)))
    print(site_list)
    joined_string = ','.join(site_list)
    result = [value.strip() for value in joined_string.split(',')]
    unique_values = list(set(result))
    for site in unique_values:
        sites.append(site)
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
               "count": count,
               "sites": sites,
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


class GeneratePdf(View):
    def get(self, request, *args, **kwargs):
        if 'start_date' in  request.session:
            start_date = request.session.get('start_date')
            end_date = request.session.get('end_date')
            if request.user.is_superuser:
                companyId = request.session.get('companyId')
                company = Company.objects.get(id=companyId)
                # user  = CustomUser.objects.get(company=company)
                response  = WasteRecord.objects.filter(company=company,entry_date__gte=start_date,entry_date__lte=end_date)
            else:
                company = Company.objects.get(name=request.user.company)
                response  = WasteRecord.objects.filter(user=request.user,entry_date__gte=start_date,entry_date__lte=end_date)
            total_liquid_waste = response.aggregate(Sum('liquid_waste'))
            total_bin_gw = response.aggregate(Sum('bin_GW'))
            total_waste = response.aggregate(Sum('total_waste'))
            respdt = HttpResponse(content_type='application/pdf')
            filename = 'waste reports'
            context = {
                'company_logo': company.company_logo,
                'start': datetime.strptime(start_date, '%Y-%m-%d %H:%M:%S').date(), 
                'end': datetime.strptime(end_date, '%Y-%m-%d %H:%M:%S').date(),
                'customer_name': 'Kalki',
                'order_id': 1233434,
                'response':response,
                'total_liquid_waste':total_liquid_waste,
                'total_waste':total_waste,
                'total_bin_gw':total_bin_gw
            }
            print(context)
            # pdf = render_to_pdf('pdf/invoice.html', data)
             
            # pdf = render_to_pdf('pdf/invoice.html', context)
            # return HttpResponse(pdf, content_type='application/pdf')
            result = generate_pdf('pdf/invoice.html',file_object=respdt,context=context)
            result['Content-Disposition'] = 'attachment; filename="{}.pdf"'.format(filename)
            return result
        else:
            messages.info(request, 'Please select month and year.')
        # del request.session['start_date']
        return render(request, 'monthly-waste-report.html')
    

def AddDocuments(request):
    if request.method =='POST':
        title = request.POST.get('title')
        description = request.POST.get('description')
        file = request.FILES.get('document')
        print(file)
        docObj = Document.objects.create(
            title=title,
            description=description, 
            file=file,
        )
        messages.success(request, 'The document “{}” was added successfully.'.format(docObj))
        return redirect('/compliance_records')
    return render(request, 'compliance-certificate-download.html')

def DocumentUpdate(request, id):
    document_Obj = Document.objects.get(id=id)

    if request.method =='POST':
        document_Obj.title = request.POST['title']
        document_Obj.description = request.POST['description']

        if len(request.FILES) != 0:
            if len(document_Obj.file) > 0:
                os.remove(document_Obj.file.path)
            document_Obj.file = request.FILES['document']

        document_Obj.save()
        messages.success(request, 'The Document was changed successfully..')
        return redirect('/compliance_records')
    else:
        context = {'document_Obj': document_Obj}
    return render(request, 'compliance-certificate-download.html', context)

def DelDocument(request, id):
    document_Obj =  Document.objects.get(id=id)
    document_Obj.delete()
    messages.warning(request, 'The Document “{}” was deleted successfully.'.format(document_Obj))
    return redirect('/compliance_records')