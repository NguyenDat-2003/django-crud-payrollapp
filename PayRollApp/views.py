from django.shortcuts import redirect, render
from PayRollApp.forms import EmployeeForm
from PayRollApp.models import Employee


# Create your views here.
def EmployeesList(request):
  context = { 'employees':  Employee.objects.select_related('EmpDepartment', 'EmpCountry').all()}
#   employees = Employee.objects.select_related('EmpDepartment', 'EmpCountry').all()
#   print(employees.query)
  return render(request,'PayRollApp/EmployeesList.html',context)

def EmployeeDetail(request,id):
    employee = Employee.objects.select_related('EmpDepartment', 'EmpCountry').all().filter(id=id)
    context = {'employee': employee[0]}
    return render(request,'PayRollApp/EmployeeDetail.html',context)

def EmployeeDelete(request,id):
    employee = Employee.objects.select_related('EmpDepartment','EmpCountry').all().filter(id=id)
    context={"employee":employee[0]}   
    if request.method == "POST":
        employee.delete()
        return redirect('EmployeesList')
    
    return render(request,'PayRollApp/EmployeeDelete.html',context)


def EmployeeUpdate(request,id):
    employee = Employee.objects.select_related('EmpDepartment','EmpCountry').all().filter(id=id)
    form = EmployeeForm(instance=employee[0])
    context={"form":form}

    if request.method=="POST":        
        form = EmployeeForm(request.POST,instance=employee[0])
        if form.is_valid():
            form.save()
        return redirect("EmployeesList")
    
    return render(request,"PayRollApp/EmployeeUpdate.html",context)

def EmployeeInsert(request):
    form = EmployeeForm()
    context={"form":form}

    if request.method=="POST":        
        form = EmployeeForm(request.POST)
        if form.is_valid():
            form.save()
        return redirect("EmployeesList")
    
    return render(request,"PayRollApp/EmployeeInsert.html",context)
