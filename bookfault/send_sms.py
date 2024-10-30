from twilio.rest import Client
from .models import bookfaultmodel
import os
from dotenv import load_dotenv

def readfile():
    with open('my_file.txt', 'r') as fp:
        content = fp.read()
    return content

def msgsend():

    obj = bookfaultmodel.objects.all().values().last()
    not_requred = ['Fault_Restored_Date_Time','SJC_Used','OFC_Used','OFC_Type','PLB_Used','Trial_Pit','Trench','Reason_Of_Fault' ,'is_updated']
    filtered_dict = {key: value for key, value in obj.items() if key not in not_requred}
    with open('my_file.txt', 'w') as f:
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





