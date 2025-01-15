from django.urls import path
from PayRollApp import views

urlpatterns = [
  path("EmployeesList",views.EmployeesList,name="EmployeesList"),
  path("EmployeeDetail/<int:id>",views.EmployeeDetail,name="EmployeeDetail"),
  path("EmployeeDelete/<int:id>",views.EmployeeDelete,name="EmployeeDelete"),
  path("EmployeeUpdate/<int:id>",views.EmployeeUpdate,name="EmployeeUpdate"),
  path("EmployeeInsert",views.EmployeeInsert,name="EmployeeInsert"),
  path("BulkEmployeeInsert",views.BulkEmployeeInsert,name="BulkEmployeeInsert"),
  path("NewBulkEmployeeInsertFormSet",views.NewBulkEmployeeInsertFormSet,name="NewBulkEmployeeInsertFormSet"),

]
