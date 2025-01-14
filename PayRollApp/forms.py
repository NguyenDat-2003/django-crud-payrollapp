from PayRollApp.models import Employee
from django import forms

class EmployeeForm(forms.ModelForm):
  class Meta:
    model=Employee
    fields='__all__'
    widgets = {
            'BirthDate': forms.widgets.DateInput(attrs={'type': 'date'}),
            'HireDate': forms.widgets.DateInput(attrs={'type': 'date'}),
        }
