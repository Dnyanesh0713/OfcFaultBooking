from pyexpat.errors import messages
from twilio.rest import Client
from .models import bookfaultmodel
import os
from dotenv import load_dotenv
from django.utils import timezone
from datetime import date


def get_non_restored_faults_summary():
    # Get all non-restored faults grouped by SDCA
    faults = bookfaultmodel.objects.filter(is_updated=False)

    summary1 = "*Daily Non-Restored Faults Report*\n\n"
    summary2 = "*Daily Non-Restored Faults Report*\n\n"
    grouped_faults = {}

    for fault in faults:
        grouped_faults.setdefault(fault.SDCA, []).append(fault)

    for sdca, sdca_faults in grouped_faults.items():
        if sdca in ['Jamkhed','Karjat','Parner','Pathardi','Shevgaon','Shrigonda','ANR']:
            summary1 += f"*SDCA: {sdca}*\n"
            for idx, fault in enumerate(sdca_faults, start=1):  # Enumerate faults for numbering
                summary1 += f"{idx}. {fault.Routename}\n"
        else:
            summary2 += f"*SDCA: {sdca}*\n"
            for idx, fault in enumerate(sdca_faults, start=1):  # Enumerate faults for numbering
                summary2 += f"{idx}. {fault.Routename}\n"

    print(summary1)
    print(summary2)
    return summary1,summary2


def readfile():
    with open('my_file.txt', 'r') as fp:
        content = fp.read()
    return content

def msgsend():

    obj = bookfaultmodel.objects.all().values().last()
    not_requred = ['Fault_Restored_Date_Time','SJC_Used','OFC_Used','OFC_Type','PLB_Used','Trial_Pit','Trench','Reason_Of_Fault' ,'is_updated','Total_downtime','Transnet_ID','Admin_Remarks','latitude','longitude',]
    # Convert `Reporting_date_time` to local time (IST) if it exists
    filtered_dict = {}
    for key, value in obj.items():
        if key == 'Reporting_date_time' and value:
            utc_datetime = value  # Assuming `value` is in UTC
            local_datetime = timezone.localtime(utc_datetime, timezone.get_current_timezone())
            filtered_dict[key] = local_datetime.strftime('%Y-%m-%d %H:%M:%S')
        elif key not in not_requred:
            filtered_dict[key] = value

    # Write the filtered dictionary to the text file
    with open('my_file.txt', 'w', encoding='utf-8') as f:
        f.write(f'''*"Fault Alert...!!!" Your {filtered_dict['Routename'].upper()} Route Failed please restore it on priority.*\n''')
        for key, value in filtered_dict.items():
            f.write(f'{key}: {value}\n')

    load_dotenv()  # Load environment variables from .env file
    account_sid = os.environ.get('account_sid')
    auth_token = os.environ.get('auth_token')

    client = Client(account_sid, auth_token)
    client.messages.create(
    body= '{}'.format(readfile()),
    from_='whatsapp:+14155238886',
    to='whatsapp:+917588380713'
    )
    # sendwpmsg()

#**********************************************************************************************************************
#*****************************For Sytem fault Messages*****************************************************************
def msgsend_system_fault():
    obj = bookfaultmodel.objects.all().values().last()
    not_requred = ['Fault_Restored_Date_Time', 'SJC_Used', 'OFC_Used', 'OFC_Type', 'PLB_Used', 'Trial_Pit', 'Trench',
                   'Reason_Of_Fault', 'is_updated', 'Total_downtime', 'Transnet_ID', 'Admin_Remarks','latitude','longitude',]
    # Convert `Reporting_date_time` to local time (IST) if it exists
    filtered_dict = {}
    for key, value in obj.items():
        if key == 'Reporting_date_time' and value:
            utc_datetime = value  # Assuming `value` is in UTC
            local_datetime = timezone.localtime(utc_datetime, timezone.get_current_timezone())
            filtered_dict[key] = local_datetime.strftime('%Y-%m-%d %H:%M:%S')
        elif key not in not_requred:
            filtered_dict[key] = value

    # Write the filtered dictionary to the text file
    with open('my_file.txt', 'w', encoding='utf-8') as f:
        f.write(f'''*"Fault Alert...!!!" Your {filtered_dict['Routename'].upper()} Route Sysyem Failed.*\n''')
        for key, value in filtered_dict.items():
            f.write(f'{key}: {value}\n')

    load_dotenv()  # Load environment variables from .env file
    account_sid = os.environ.get('account_sid')
    auth_token = os.environ.get('auth_token')

    client = Client(account_sid, auth_token)
    client.messages.create(
        body='{}'.format(readfile()),
        from_='whatsapp:+14155238886',
        to='whatsapp:+917588380713'
    )

#**********************************************************************************************************************
#*****************************For geting restoration message **********************************************************

def readfile_restore():
    with open('my_file2.txt', 'r') as fp:
        content = fp.read()
    return content

def restorationmsg(date):

    # Fetch the specific record by date
    try:
        obj = bookfaultmodel.objects.get(Fault_Restored_Date_Time=date)
    except bookfaultmodel.DoesNotExist:
        print("No record found for the provided date.")
        obj = None

    not_required_items = ['Traffic_Affected', 'Remarks', 'is_updated', 'Transnet_ID', 'Admin_Remarks']

    if obj:
        filtered_dict = {}

        # Add all fields except Reporting_date_time and Fault_Restored_Date_Time first
        for field in obj._meta.fields:
            field_name = field.name
            if field_name not in not_required_items and field_name not in ['Reporting_date_time',
                                                                           'Fault_Restored_Date_Time']:
                filtered_dict[field_name] = getattr(obj, field_name)

        # Add Fault_Restored_Date_Time and Reporting_date_time at the second-to-last position
        if obj.Reporting_date_time:
            utc_datetime = obj.Reporting_date_time  # Assuming this is in UTC
            local_datetime = timezone.localtime(utc_datetime, timezone.get_current_timezone())
            filtered_dict['Reporting_date_time'] = local_datetime.strftime('%Y-%m-%d %H:%M:%S')

        if obj.Fault_Restored_Date_Time:
            utc_datetime = obj.Fault_Restored_Date_Time  # Assuming this is in UTC
            local_datetime = timezone.localtime(utc_datetime, timezone.get_current_timezone())
            filtered_dict['Fault_Restored_Date_Time'] = local_datetime.strftime('%Y-%m-%d %H:%M:%S')

        # Write the filtered dictionary to the text file
        with open('my_file2.txt', 'w', encoding='utf-8') as f:
            f.write(
                f'''*"Good News...!!!" Your {filtered_dict['Routename'].upper()} Route Fault Restored Successfully Please find below the details of material used:.*\n''')
            for key, value in filtered_dict.items():
                f.write(f'{key}: {value}\n')

        load_dotenv()  # Load environment variables from .env file
        account_sid = os.environ.get('account_sid')
        auth_token = os.environ.get('auth_token')

        client = Client(account_sid, auth_token)
        client.messages.create(
            body='{}'.format(readfile_restore()),
            from_='whatsapp:+14155238886',
            to='whatsapp:+917588380713'
        )

#**************************************************************************************************************************
#****************************For Daily schedule of messages ******************************************************************

def send_whatsapp_message(summary):
    load_dotenv()  # Load environment variables from .env file
    account_sid = os.environ.get('account_sid')
    auth_token = os.environ.get('auth_token')

    client = Client(account_sid, auth_token)
    client.messages.create(
        body=summary,
        from_='whatsapp:+14155238886',
        to='whatsapp:+917588380713'
    )
