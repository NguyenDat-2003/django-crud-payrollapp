from django.shortcuts import redirect, render
from PayRollApp.forms import EmployeeForm,PartTimeEmployeeForm,PartTimeEmployeeFormSet
from PayRollApp.models import Employee,PartTimeEmployee


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

def BulkEmployeeInsert(request):
    extra_forms = 10
    Status=''

    forms = [PartTimeEmployeeForm(request.POST or None, prefix=f'employee-{i}')  for i in range(extra_forms)]

    if request.method=="POST":        
        for form in forms:
            if form.is_valid() and form.cleaned_data.get('FirstName', '') :
                form.save()
                Status='Records were inserted successfully..'
            
    
    return render(request,"PayRollApp/PartTimeEmployeeList.html",{"forms" : forms, "Status" : Status })

def NewBulkEmployeeInsertFormSet(request):
    if request.method == "POST":
        formset = PartTimeEmployeeFormSet(request.POST)
        if formset.is_valid():
            employees = formset.save(commit=False)
            PartTimeEmployee.objects.bulk_create(employees)
            return redirect('NewBulkEmployeeInsertFormSet')
    else:
        formset = PartTimeEmployeeFormSet(queryset=PartTimeEmployee.objects.none())
            
    
    return render(request,"PayRollApp/NewBulkInsert.html",{"formset": formset})
