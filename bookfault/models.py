from django.db import models
from django.utils import timezone
from django.contrib import messages
from django.core.exceptions import ValidationError
from .fields import FormattedDateTimeField
from datetime import timedelta
import re
from django.utils.safestring import mark_safe

FAULT_CHOICES = (
    ('1','Select the type of fault'),
    ('SYSTEM','SYSTEM'),
    ('OFC CUT', 'OFC CUT'),
    ('SINGLE FIBRE', 'SINGLE FIBRE'),
    ('PATCH CHORD','PATCH CHORD'),
    ('POWER LOSS','POWER LOSS'),
    ('BBNL OFC CUT','BBNL OFC CUT'),
    ('MAHA_IT OFC CUT','MAHA_IT OFC CUT'),
)

SDCA_CHOICES = (
    ('1', 'Select your SDCA'),
    ('ANR', 'ANR'),
    ('Akole', 'Akole'),
    ('Jamkhed', 'Jamkhed'),
    ('Karjat', 'Karjat'),
    ('Kopergaon', 'Kopergaon'),
    ('Nevasa', 'Nevasa'),
    ('Parner', 'Parner'),
    ('Pathardi', 'Pathardi'),
    ('Rahuri', 'Rahuri'),
    ('Rahata', 'Rahata'),
    ('Sangamner', 'Sangamner'),
    ('Shevgaon', 'Shevgaon'),
    ('Shrirampur', 'Shrirampur'),
    ('Shrigonda', 'Shrigonda'),

)

class bookfaultmodel(models.Model):
    SDCA = models.CharField(max_length=50, choices=SDCA_CHOICES, default='1', null=False)
    Routename = models.CharField(max_length=100, null=False)
    FaultType = models.CharField(max_length=100, choices=FAULT_CHOICES, default='1', null=False)
    Reporting_date_time = FormattedDateTimeField(null=False)
    Traffic_Affected = models.TextField(null=False)
    Remarks = models.TextField(null=True,blank=True)

    Fault_Restored_Date_Time = FormattedDateTimeField(null=True,blank=True)
    SJC_Used = models.CharField(max_length=2,null=False,default='')
    OFC_Used = models.CharField(max_length=4,null=False,default='')
    OFC_Type = models.CharField(max_length=10, null=False,default='')
    PLB_Used = models.CharField(max_length=4,null=False,default='')
    Trial_Pit = models.CharField(max_length=2,null=False,default='')
    Trench = models.CharField(max_length=10,null=False,default='')
    Reason_Of_Fault = models.CharField(max_length=100, null=False,default='')
    Total_downtime = models.CharField(max_length=50,editable=False,default='')
    Transnet_ID = models.CharField(max_length=10,null=True,blank=True,default='')
    latitude = models.DecimalField(max_digits=10, decimal_places=7, null=True, blank=True)
    longitude = models.DecimalField(max_digits=10, decimal_places=7, null=True, blank=True)
    Admin_Remarks = models.TextField(null=True,blank=True,default='')
    is_updated = models.BooleanField(null=False,default=False)


    def __str__(self):
        return str(self.Fault_Restored_Date_Time) if self.Fault_Restored_Date_Time else "No Date"

#**********Before saving the Form added constraints on Date Time Field To check date and time is not in future*********

    def clean(self):
        # Define any comparison dates or datetime fields
        current_time = timezone.localtime(timezone.now())
        # Format both dates to `DD-MM-YY :: HH:MM` for the error message
        formatted_current_time = current_time.strftime("%d-%m-%Y :: %I:%M %p")
        formatted_reporting_time = self.Reporting_date_time.strftime("%d-%m-%Y :: %I:%M %p")

        # Check if the Reporting_date_time is in the future
        if self.Reporting_date_time:
            if self.Reporting_date_time > current_time:
                raise ValidationError(
                    f"The entered date and time must not exceed {formatted_current_time}"
                    )
        # Check if the Restored_date_time is in the future
        if self.Fault_Restored_Date_Time:
            if self.Fault_Restored_Date_Time > current_time:
                raise ValidationError(
                    f"The entered date and time must not exceed {formatted_current_time}"
                )
        # Calculate downtime only if both dates are set
        if self.Fault_Restored_Date_Time and self.Reporting_date_time:
            if self.Reporting_date_time < self.Fault_Restored_Date_Time:
                downtime = calculate_downtime(self.Fault_Restored_Date_Time, self.Reporting_date_time)
                self.Total_downtime = downtime
            else:
                raise ValidationError(
                    "The Fault Restored Date and Time must occur after the Fault Reporting Date and Time."
                )

        #Logic to store the Routename in the desired format and not as entered..
        if self.Routename:
            route_name = self.Routename.strip().lower()
            route_name = route_name.replace(" to ", " - ")
            route_name = re.sub(r'\s*-\s*', ' - ', route_name)  # Normalize spacing around '-'
            parts = route_name.split(" - ")
            route_name = " - ".join(sorted(parts))
            self.Routename = route_name

        existing_fault = bookfaultmodel.objects.filter(
            Routename__iexact=self.Routename,
            is_updated=False
        ).exclude(id=self.id).first()

        if existing_fault:
            raise ValidationError(
                mark_safe(
                    f"A fault with the same route already exists with:<br>"
                    f"Fault ID: <strong>{existing_fault.id}</strong><br>"
                    f"Route Name: <strong>{existing_fault.Routename}</strong><br>"
                    f"SDCA: <strong>{existing_fault.SDCA}</strong><br>"
                    "It is not restored yet."
                )
            )

    def save(self, *args, **kwargs):
        # Call the clean method to enforce validation before saving
        self.clean()
        super().save(*args, **kwargs)

#*************************** Calculate Downtime where you are Updating the Fault****************************************

def calculate_downtime(FRDT,RDT):
    # Calculate downtime if Fault_Restored_Date_Time is set
    if FRDT and RDT:
        downtime = FRDT - RDT
        days = downtime.days
        hours, remainder = divmod(downtime.seconds, 3600)
        minutes = remainder // 60

        # Format downtime as "X days, X hours, X minutes"
        Total_downtime = f"{days} days, {hours} hours, {minutes} minutes"
    else:
        Total_downtime = ""  # Clear if no restored date
    return Total_downtime
