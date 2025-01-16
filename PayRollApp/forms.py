from PayRollApp.models import Employee, OnSiteEmployees,PartTimeEmployee
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

class OnSiteEmployeesForm(forms.ModelForm):
    class Meta:
        model = OnSiteEmployees
        fields = ['first_name', 'last_name', 'country', 'state', 'city']

        widgets = {
            'first_name': forms.TextInput(attrs={
                'class': "form-control",
                'style': 'max-width: 300px;',
                'placeholder': 'First Name'
                }),
             'last_name': forms.TextInput(attrs={
                'class': "form-control",
                'style': 'max-width: 300px;',
                'placeholder': 'Last Name'
                }),
            'country': forms.Select(attrs={
                'class': "form-control", 
                'style': 'max-width: 300px;',
                'placeholder': 'Country'

                }),
            'state': forms.Select(attrs={
                'class': "form-control", 
                'style': 'max-width: 300px;',
                'placeholder': 'state'
                }),
            'city': forms.Select(attrs={
                'class': "form-control", 
                'style': 'max-width: 300px;',
                'placeholder': 'city'
                })
         }
