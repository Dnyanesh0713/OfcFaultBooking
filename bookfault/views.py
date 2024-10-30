
from django.shortcuts import render,redirect,get_object_or_404
from .models import bookfaultmodel
from .forms import bookfaultform,restoreform,updateform,updateadminform
from django.http import HttpResponse
from .send_sms import msgsend
from .send_email import send_email_with_attachment
from django.utils import timezone
from openpyxl import Workbook
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ValidationError
import re
from django.db import IntegrityError
import tempfile

def loginhome(r):
    if r.method == 'POST':
        if r.user.is_authenticated:
            return redirect('/home/')  # Redirect if already logged in
    return render(r,'auths/login.html')


#************************************************************************************************************************
#*******************Uses to send whatsapp sms to a number according to SDCA FRT teams************************************
def sortsdca(sdca):
    if sdca in ['Jamkhed','Karjat']:
        msgsend() # Send whats app message to the registered number for Jamkhed SDCA
    else:
        pass

#************************************************************************************************************************
#****************************Dislay Home, all tabs in base.html extended to index html**********************************
@login_required
def home(r):
    return render(r,'index.html')

#************************************************************************************************************************
#************************Uses to show fault booking form and triggering message sending funtion.(base_book.html extended to bookfault.html)*************************

def OfcFaultView(r):
    form = bookfaultform()
    if r.method == 'POST':
        form = bookfaultform(r.POST)
        if form.is_valid():
            form.save()
            sortsdca(r.POST['SDCA'])
            obj = bookfaultmodel.objects.all().values_list('id').last()
            success_message = f"Your fault has been submitted successfully! Your Fault id is: {obj[0]}"  # Success message
            messages.success(r, success_message)  # Add message to be shown in the modal
            return redirect("/bookfault/")  # Redirect after successful submission
    return render(r,'bookfault/bookfault.html',{'form':form})

#************************************************************************************************************************
#***********************Calling funtion of email_send module to send the email******************************************
# def GetReport(r):
#     send_email_with_attachment() #Send the Email to given mail id
#     success_message = "Your Email has been sent successfully!"  # Success message
#     messages.success(r,success_message)  # Add message to be shown in the modal
#     return redirect("/home/")  # Redirect after successful submission

#************************************************************************************************************************
#*******************This funtion is used to display single field form and catch id entered by restoration team to update particular fault********************
#*******************(base_restore.html extended to restorefault.html)*************************************************************************
def FaultRestoredView(r):
    global id
    form = restoreform()
    if r.method == 'POST':
        form = restoreform(r.POST)
        if form.is_valid():
            id = form.cleaned_data['Fault_ID']
            # Try to find the object; if it doesn't exist, handle the exception
            try:
                # Attempt to retrieve the object to confirm it exists
                bookfaultmodel.objects.get(id=id)
                return redirect("/display/")  # Proceed if the object exists
            except bookfaultmodel.DoesNotExist:
                # Display an error message to the user
                messages.error(r, "Fault with ID {} does not exist.".format(id))
    return render(r, 'restorefault/restorefault.html', {'form': form})


#************************************************************************************************************************
#*************used to Display the fault that has to be updated by FRT, update link provided in display.html*****************
def displayrec(r):
    object = bookfaultmodel.objects.get(id = id)
    return render(r, 'restorefault/display.html', {'object': [object]})

#************************************************************************************************************************
#*****************************Updating the form or filling the fault details which is restored by FRT*********************************************
def updaterec(r,id):

    objects = bookfaultmodel.objects.get(id=id)
    form = updateform(instance=objects)
    if r.method == 'POST':
        form = updateform(r.POST,instance=objects)
        if form.is_valid():
            if form.cleaned_data['Fault_Restored_Date_Time'] is None:
                form.add_error('Fault_Restored_Date_Time', 'Please select Fault restored Date and Time.')  # Custom error
            elif form.cleaned_data['is_updated'] == False:
                form.add_error('is_updated', 'Please Click on checkbox then submit.')  # Custom error
            else:
                form.save()
                success_message = "Your fault Restoration Report has been submitted successfully!"  # Success message
                messages.success(r, success_message)  # Add message to be shown in the modal
                return redirect("/faultrestore/")  # Redirect after successful submission
    return render(r,'restorefault/update.html',{'form':form})


#************************************************************************************************************************
#*******************Update fault by Admin********************************************************************************

def updateadmin(r,id):

    objects = bookfaultmodel.objects.get(id=id)
    form = updateadminform(instance=objects)
    if r.method == 'POST':
        form = updateadminform(r.POST,instance=objects)
        if form.is_valid():
            if form.cleaned_data['Fault_Restored_Date_Time'] is None:
                form.add_error('Fault_Restored_Date_Time', 'Please select Fault restored Date and Time.')  # Custom error
            elif form.cleaned_data['is_updated'] == False:
                form.add_error('is_updated', 'Please Click on checkbox then submit.')  # Custom error
            else:
                form.save()
                success_message = "Your fault Restoration Report has been Updated successfully!"  # Success message
                messages.success(r, success_message)  # Add message to be shown in the modal
                return redirect("/home/")  # Redirect after successful submission
    return render(r,'restorefault/update.html',{'form':form})

#************************************************************************************************************************
#*******************Delete a particular fault here***********************************************************************
def deletefault(r,id):
    #objects = bookfaultmodel.objects.get(id = id)
    objects = get_object_or_404(bookfaultmodel, id=id)
    objects.delete()
    success_message = "Your Fault has been Deleted successfully!"  # Success message
    messages.success(r, success_message)  # Add message to be shown in the modal
    return redirect("/home/")

#************************************************************************************************************************
#******************Download Excel Facility is added here ****************************************************************

def export_to_excel(queryset,flg, filename="data_export.xlsx"):
    # Create a new workbook and add a worksheet
    workbook = Workbook()
    worksheet = workbook.active
    worksheet.title = "Data Export"

    # Add headers to the worksheet
    headers = [
        'Fault ID', 'SDCA', 'Routename', 'FaultType', 'Reporting Date Time',
        'Traffic Affected', 'Remarks', 'Fault Restored Date Time', 'SJC Used',
        'OFC Used', 'OFC Type', 'PLB Used', 'Trial Pit', 'Trench',
        'Reason Of Fault', 'Restored Status'
    ]
    worksheet.append(headers)

    # Write data to worksheet
    for obj in queryset:
        row = [
            obj.id,
            obj.SDCA,
            obj.Routename,
            obj.FaultType,
            obj.Reporting_date_time.replace(tzinfo=None) if obj.Reporting_date_time else None,
            obj.Traffic_Affected,
            obj.Remarks,
            obj.Fault_Restored_Date_Time.replace(tzinfo=None) if obj.Fault_Restored_Date_Time else None,
            obj.SJC_Used,
            obj.OFC_Used,
            obj.OFC_Type,
            obj.PLB_Used,
            obj.Trial_Pit,
            obj.Trench,
            obj.Reason_Of_Fault,
            "Restored" if obj.is_updated else "Not Restored"
        ]
        worksheet.append(row)
    if flg == 1:
        # Save excel file temporary
        temp_file = tempfile.NamedTemporaryFile(suffix=".xlsx", delete=False)
        workbook.save(temp_file.name)
        return  temp_file.name
    else:

        # Set up the response as an Excel file
        response = HttpResponse(
            content_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        )
        response["Content-Disposition"] = f'attachment; filename="{filename}"'
        workbook.save(response)
        return response

#************************************************************************************************************************
#******************** Display diff category of faults and Download Functions logic*************************************************************

def displayallfaults(r):
    # Get sorting parameters from the request
    sort_by = r.GET.get('sort_by')
    order = r.GET.get('order','asc')
    # If sorting parameters are present, add ordering
    if sort_by and order:
        if order == 'desc':
            objects = bookfaultmodel.objects.all().order_by(f'-{sort_by}')
        else:
            objects = bookfaultmodel.objects.all().order_by(sort_by)
    else:
        # Define the queryset without ordering by default
        objects = bookfaultmodel.objects.all()

    if r.GET.get('download') == 'true':  # Check if download is requested
        flag = 0
        return export_to_excel(objects,flag, filename="All_Faults.xlsx")

    if r.GET.get('email') == 'true':  # Check if email is requested
        flag = 1
        flname = "All_Faults.xlsx"
        tmpfile = export_to_excel(objects,flag, filename="All_Faults.xlsx")
        send_email_with_attachment(tmpfile,flname)
        success_message = "Your Email has been sent successfully!"  # Success message
        messages.success(r,success_message)  # Add message to be shown in the modal
        return redirect("/home/")  # Redirect after successful submission

    return render(r, "Displayfault/viewfaults.html", {"objects": objects, "sort_by": sort_by,"order": order})

def displaydailyfaults(r):
    today = timezone.now().date()
    # Get sorting parameters from the request
    sort_by = r.GET.get('sort_by')
    order = r.GET.get('order','asc')
    # If sorting parameters are present, add ordering
    if sort_by and order:
        if order == 'desc':
            objects = bookfaultmodel.objects.filter(Reporting_date_time__date=today).order_by(f'-{sort_by}')
        else:
            objects = bookfaultmodel.objects.filter(Reporting_date_time__date=today).order_by(sort_by)
    else:
        # Define the queryset without ordering by default
        objects = bookfaultmodel.objects.filter(Reporting_date_time__date=today)

    if r.GET.get('download') == 'true':  # Check if download is requested
        flag = 0
        return export_to_excel(objects, flag, filename="Daily_Faults.xlsx")

    if r.GET.get('email') == 'true':  # Check if email is requested
        flag = 1
        flname = "Daily_Faults.xlsx"
        tmpfile = export_to_excel(objects,flag, filename="Daily_Faults.xlsx")
        send_email_with_attachment(tmpfile,flname)
        success_message = "Your Email has been sent successfully!"  # Success message
        messages.success(r,success_message)  # Add message to be shown in the modal
        return redirect("/home/")  # Redirect after successful submission
    return render(r, "Displayfault/viewfaults.html", {"objects": objects, "sort_by": sort_by,"order": order})

def displaymonthlyfaults(r):
    now = timezone.now()
    # Get sorting parameters from the request
    sort_by = r.GET.get('sort_by')
    order = r.GET.get('order','asc')
    # If sorting parameters are present, add ordering
    if sort_by and order:
        if order == 'desc':
            objects = bookfaultmodel.objects.filter(Reporting_date_time__year=now.year,Reporting_date_time__month=now.month).order_by(f'-{sort_by}')
        else:
            objects = bookfaultmodel.objects.filter(Reporting_date_time__year=now.year,Reporting_date_time__month=now.month).order_by(sort_by)
    else:
        # Define the queryset without ordering by default
        objects = bookfaultmodel.objects.filter(Reporting_date_time__year=now.year,Reporting_date_time__month=now.month)
    if r.GET.get('download') == 'true':  # Check if download is requested
        flag = 0
        return export_to_excel(objects, flag, filename="Monthly_Faults.xlsx")

    if r.GET.get('email') == 'true':  # Check if email is requested
        flag = 1
        flname = "Monthly_Faults.xlsx"
        tmpfile = export_to_excel(objects,flag, filename="Monthly_Faults.xlsx")
        send_email_with_attachment(tmpfile,flname)
        success_message = "Your Email has been sent successfully!"  # Success message
        messages.success(r,success_message)  # Add message to be shown in the modal
        return redirect("/home/")  # Redirect after successful submission
    return render(r, "Displayfault/viewfaults.html", {"objects": objects, "sort_by": sort_by,"order": order})

def displaynotrestored(r):
    # Get sorting parameters from the request
    sort_by = r.GET.get('sort_by')
    order = r.GET.get('order','asc')
    # If sorting parameters are present, add ordering
    if sort_by and order:
        if order == 'desc':
            objects = bookfaultmodel.objects.filter(is_updated=False).order_by(f'-{sort_by}')
        else:
            objects = bookfaultmodel.objects.filter(is_updated=False).order_by(sort_by)
    else:
        # Define the queryset without ordering by default
        objects = bookfaultmodel.objects.filter(is_updated=False)

    if r.GET.get('download') == 'true':  # Check if download is requested
        flag = 0
        return export_to_excel(objects, flag, filename="Not_Restored_faults.xlsx")

    if r.GET.get('email') == 'true':  # Check if email is requested
        flag = 1
        flname = "Not_Restored_faults.xlsx"
        tmpfile = export_to_excel(objects,flag, filename="Not_Restored_faults.xlsx")
        send_email_with_attachment(tmpfile,flname)
        success_message = "Your Email has been sent successfully!"  # Success message
        messages.success(r,success_message)  # Add message to be shown in the modal
        return redirect("/home/")  # Redirect after successful submission
    return render(r, "Displayfault/viewfaults.html", {"objects": objects, "sort_by": sort_by,"order": order})

#*************************************************************************************************************************************
#******************************Register User Logic written here *****************************************************************

def validate_email(email):
    # Simple regex for validating email format
    email_regex = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return re.match(email_regex, email)

def validate_mobile(mobile):
    # Regex for validating Indian mobile number format (10 digits)
    mobile_regex = r'^[789]\d{9}$'  # Starts with 7, 8, or 9 and followed by 9 digits
    return re.match(mobile_regex, mobile)

def register(request):
    if request.method == 'POST':
        first_name = request.POST['first_name']
        middle_name = request.POST.get('middle_name', '')  # Optional
        last_name = request.POST['last_name']
        mobile = request.POST['mobile']
        sdca = request.POST['sdca']
        post = request.POST['post']
        email = request.POST['email']
        password = request.POST['password']
        confirm_password = request.POST['confirm_password']

        # Validate email
        if not validate_email(email):
            messages.error(request, "Please enter a valid email address.")
            return render(request, 'auths/register.html')

        # Validate mobile number
        if not validate_mobile(mobile):
            messages.error(request, "Please enter a valid mobile number (10 digits).")
            return render(request, 'auths/register.html')

        # Validate password
        if password != confirm_password:
            messages.error(request, "Passwords do not match.")
            return render(request, 'auths/register.html')

        # Create the user
        try:
            # Check if the user with this email already exists
            if User.objects.filter(username=email).exists():
                messages.error(request, "This email is already registered. Please use a different email.")
                return render(request, 'auths/register.html')

            user = User.objects.create_user(
                username=email,  # Use email as username
                password=password,
                first_name=first_name,
                last_name=last_name
            )
            user.email = email  # Set the email field
            user.save()

            messages.success(request, "Registration successful! You can now log in with this user ID and Password.")
            return redirect('/home/')  # Redirect to login page
        except IntegrityError:
            messages.error(request, "This email is already registered. Please use a different email.")
        except ValidationError as e:
            messages.error(request, str(e))

    return render(request, 'auths/register.html')


#*************************************************************************************************************************************
#******************************Login and Logout User Logic written here *****************************************************************

def user_login(request):
    image_range = range(1, 11)  # Create a range from 1 to 10
    if request.method == 'POST':
        # Check if user is already authenticated
        if request.user.is_authenticated:
            return redirect('/home/')  # Redirect if already logged in
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('/home/')  # Redirect to a home page or dashboard
        else:
            return render(request, 'auths/login.html', {'error': 'Invalid credentials'})
    return render(request, 'auths/login.html',{'image_range': image_range})


def user_logout(request):
    logout(request)
    return redirect('/login/')  # Redirect to the login page