from django.db import models

FAULT_CHOICES = (
    ('1','Select the type of fault'),
    ('SYSTEM','SYSTEM'),
    ('OFC CUT', 'OFC CUT'),
    ('PATCH CHORD','PATCH CHORD'),
)

SDCA_CHOICES = (
    ('1', 'Select your SDCA'),
    ('Ahilyanagar', 'Ahilyanagar'),
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
    Reporting_date_time = models.DateTimeField(null=False)
    Traffic_Affected = models.TextField(null=False)
    Remarks = models.TextField(null=True,blank=True)

    Fault_Restored_Date_Time = models.DateTimeField(null=True,blank=True)
    SJC_Used = models.CharField(max_length=2,null=False,default='')
    OFC_Used = models.CharField(max_length=4,null=False,default='')
    OFC_Type = models.CharField(max_length=10, null=False,default='')
    PLB_Used = models.CharField(max_length=4,null=False,default='')
    Trial_Pit = models.CharField(max_length=2,null=False,default='')
    Trench = models.CharField(max_length=10,null=False,default='')
    Reason_Of_Fault = models.CharField(max_length=100, null=False,default='')
    is_updated = models.BooleanField(null=False,default=False)

    def __str__(self):
        return str(self.Fault_Restored_Date_Time) if self.Fault_Restored_Date_Time else "No Date"

