from django.core.mail import EmailMessage
from django.shortcuts import render,redirect
from django.conf import settings
import pandas as pd
from django.db import connection
from io import BytesIO
from django.contrib import messages

def send_email_with_attachment(file,filename):

    # Subject and body of the email
    subject = f'{filename.split('.')[0]} Report'
    body = f'Please find the attached {filename.split('.')[0]} Report.'

    # Recipient email addresses
    recipients = ['dnyaneshwar0713@gmail.com']

    # Create the EmailMessage object
    email = EmailMessage(
        subject=subject,
        body=body,
        from_email=settings.DEFAULT_FROM_EMAIL,
        to=recipients,
    )

    # Path to the file you want to attach (assuming the file exists in MEDIA_ROOT)
    with open(file, 'rb') as f:
        email.attach(filename, f.read(), 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')


    # Send the email
    email.send()








