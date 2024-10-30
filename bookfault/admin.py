from django.contrib import admin

from .models import bookfaultmodel


class bookfaultadmin(admin.ModelAdmin):
    list_display = ['Routename','FaultType','SDCA','Reporting_date_time','Traffic_Affected','Remarks','Fault_Restored_Date_Time','SJC_Used','OFC_Used','OFC_Type','PLB_Used','Trial_Pit','Trench','Reason_Of_Fault']

admin.site.register(bookfaultmodel,bookfaultadmin)
