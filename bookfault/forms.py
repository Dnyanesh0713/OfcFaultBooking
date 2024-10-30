from django import forms
from .models import bookfaultmodel

#*************************Form for booking the fault all fields not shown other fields set to null*********************

class bookfaultform(forms.ModelForm):
    class Meta:
        model = bookfaultmodel
        fields = ('SDCA','Routename','FaultType','Reporting_date_time','Traffic_Affected','Remarks',)

        # widget to decorate the model form
        widgets = {

            'SDCA': forms.Select(attrs={
                'class': 'form-control',
                'style': 'width: 37%;',
           }),
            'Routename': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter Route name. (A end - B end)',
                'style': 'width: 37%;',
            }),
            'FaultType': forms.Select(attrs={'class': 'form-control', 'style': 'width: 37%;',
                                             }),
            'Reporting_date_time': forms.DateTimeInput(attrs={
                'type': 'datetime-local',
                'class': 'form-control',
                'placeholder': 'YYYY-MM-DD HH:MM',
                'style': 'width: 37%;',
            }),
            'Traffic_Affected': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 2,  # Control the height of the textarea
                'placeholder': 'Enter The Affected Trafic Details',
                'style': 'width: 37%;',
            }),
            'Remarks': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 2,  # Control the height of the textarea
                'placeholder': 'Enter Remark if any or nil',
                'style': 'width: 37%;',
            }),

            }

#**************************Form for the Entering the fault id to fetch the entire fault****************************

class restoreform(forms.Form):
    Fault_ID = forms.IntegerField(
        widget=forms.NumberInput(attrs={
            'placeholder': 'Enter the fault id you received in the fault book message',  # Placeholder text
            'style': 'width: 37%;',
            'class': 'form-control',
        })
    )

#*************************************Update form for the FRT All fields not shown and all fields not updatable*********************

class updateform(forms.ModelForm):
    class Meta:
        model = bookfaultmodel
        fields = ('SDCA','Routename','Reporting_date_time','Fault_Restored_Date_Time','SJC_Used','OFC_Used','OFC_Type','PLB_Used','Trial_Pit','Trench','Reason_Of_Fault','is_updated')

        def __init__(self, *args, **kwargs):
            # Check if an instance is being updated
            instance = kwargs.get('instance')
            super().__init__(*args, **kwargs)

            # Make the datetime_field required if the instance exists (update mode)
            if instance and instance.pk:
                self.fields['Fault_Restored_Date_Time'].required = True

        widgets = {
            'SDCA': forms.TextInput(attrs={
                'class': 'form-control',
                'style': 'width: 37%;',
                 'readonly':True,
               }),

            'Routename': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter Route name. (A end - B end)',
                'style': 'width: 37%;',
                'readonly': True,
            }),

            'Reporting_date_time': forms.DateTimeInput(attrs={
                'type': 'datetime-local',
                'class': 'form-control',
                'placeholder': 'YYYY-MM-DD HH:MM',
                'style': 'width: 37%;',
                'readonly': True,
            }),

            'Fault_Restored_Date_Time': forms.DateTimeInput(attrs={
                'type': 'datetime-local',
                'class': 'form-control',
                'placeholder': 'YYYY-MM-DD HH:MM',
                'style': 'width: 37%;',
            }),

            'SJC_Used': forms.TextInput(attrs={
                'placeholder': 'Enter the number of SJC used',  # Placeholder text
                'style': 'width: 37%;',
                'class': 'form-control',
            }),

            'OFC_Used': forms.TextInput(attrs={
                'placeholder': 'Enter the OFC used in meter',  # Placeholder text
                'style': 'width: 37%;',
                'class': 'form-control',
            }),
            'OFC_Type': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter the type of OFC used(4F,6F,12F,24F,48F)',
                'style': 'width: 37%;',
            }),

            'PLB_Used': forms.TextInput(attrs={
                'placeholder': 'Enter the PLB used in meter',  # Placeholder text
                'style': 'width: 37%;',
                'class': 'form-control',
            }),

            'Trial_Pit': forms.TextInput(attrs={
                'placeholder': 'Enter the Number of Trial Pit Required',  # Placeholder text
                'style': 'width: 37%;',
                'class': 'form-control',
            }),

            'Trench': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter the Trench made in meter',
                'style': 'width: 37%;',
            }),

            'Reason_Of_Fault': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter the reason of fault',
                'style': 'width: 37%;',

            }),

            'is_updated': forms.CheckboxInput(attrs={
                'class': 'form-check-input',
                'style': 'width: 5%;',

            }),
        }

#**************************** Update form for Admin all fields can updated ********************************************

class updateadminform(forms.ModelForm):
    class Meta:
        model = bookfaultmodel
        fields = "__all__"

        widgets = {
            'SDCA': forms.TextInput(attrs={
                'class': 'form-control',
                'style': 'width: 37%;',
                 'readonly':True,
               }),

            'Routename': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter Route name. (A end - B end)',
                'style': 'width: 37%;',
                'readonly': True,
            }),

            'Reporting_date_time': forms.DateTimeInput(attrs={
                'type': 'datetime-local',
                'class': 'form-control',
                'placeholder': 'YYYY-MM-DD HH:MM',
                'style': 'width: 37%;',
                'readonly': True,
            }),

            'FaultType': forms.Select(attrs={
                'class': 'form-control',
                'style': 'width: 37%;',
            }),

            'Traffic_Affected': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 2,  # Control the height of the textarea
                'placeholder': 'Enter The Affected Trafic Details',
                'style': 'width: 37%;',
            }),

            'Remarks': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 2,  # Control the height of the textarea
                'placeholder': 'Enter Remark if any or nil',
                'style': 'width: 37%;',
            }),

            'Fault_Restored_Date_Time': forms.DateTimeInput(attrs={
                'type': 'datetime-local',
                'class': 'form-control',
                'placeholder': 'YYYY-MM-DD HH:MM',
                'style': 'width: 37%;',
            }),

            'SJC_Used': forms.TextInput(attrs={
                'placeholder': 'Enter the number of SJC used',  # Placeholder text
                'style': 'width: 37%;',
                'class': 'form-control',
            }),

            'OFC_Used': forms.TextInput(attrs={
                'placeholder': 'Enter the OFC used in meter',  # Placeholder text
                'style': 'width: 37%;',
                'class': 'form-control',
            }),
            'OFC_Type': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter the type of OFC used(4F,6F,12F,24F,48F)',
                'style': 'width: 37%;',
            }),

            'PLB_Used': forms.TextInput(attrs={
                'placeholder': 'Enter the PLB used in meter',  # Placeholder text
                'style': 'width: 37%;',
                'class': 'form-control',
            }),

            'Trial_Pit': forms.TextInput(attrs={
                'placeholder': 'Enter the Number of Trial Pit Required',  # Placeholder text
                'style': 'width: 37%;',
                'class': 'form-control',
            }),

            'Trench': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter the Trench made in meter',
                'style': 'width: 37%;',
            }),

            'Reason_Of_Fault': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter the reason of fault',
                'style': 'width: 37%;',

            }),

            'is_updated': forms.CheckboxInput(attrs={
                'class': 'form-check-input',
                'style': 'width: 5%;',

            }),
        }