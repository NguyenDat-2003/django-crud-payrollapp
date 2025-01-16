from django.contrib import admin
from PayRollApp.models import Employee, City, State, OnSiteEmployees

# Register your models here.
admin.site.register(Employee)
admin.site.register(City)
admin.site.register(State)
admin.site.register(OnSiteEmployees)

