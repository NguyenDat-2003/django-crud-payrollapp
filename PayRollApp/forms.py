from PayRollApp.models import Employee,PartTimeEmployee
from django import forms

class EmployeeForm(forms.ModelForm):
  class Meta:
    model=Employee
    fields='__all__'
    widgets = {
            'BirthDate': forms.widgets.DateInput(attrs={'type': 'date'}),
            'HireDate': forms.widgets.DateInput(attrs={'type': 'date'}),
        }
    
PartTimeEmployeeForm = forms.modelform_factory(PartTimeEmployee, fields='__all__')

class NewPartTimeEmployeeForm(forms.ModelForm):
    class Meta:
        model=PartTimeEmployee
        fields="__all__"


PartTimeEmployeeFormSet = forms.modelformset_factory(PartTimeEmployee, form=NewPartTimeEmployeeForm,extra=10)
