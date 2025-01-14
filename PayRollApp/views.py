from django.shortcuts import redirect, render
from PayRollApp.forms import EmployeeForm
from PayRollApp.models import Employee


# Create your views here.
def EmployeesList(request):
  context = { 'employees':  Employee.objects.all()}
  return render(request,'PayRollApp/EmployeesList.html',context)

def EmployeeDetail(request,id):
    employee = Employee.objects.get(id=id)          
    context={'employee':employee}   
    return render(request,'PayRollApp/EmployeeDetail.html',context)

def EmployeeDelete(request,id):
    employee = Employee.objects.get(id=id)
    context={"employee":employee}   

    if request.method == "POST":
        employee.delete()
        return redirect('EmployeesList')
    
    return render(request,'PayRollApp/EmployeeDelete.html',context)


def EmployeeUpdate(request,id):
    employee = Employee.objects.get(id=id)  
    form = EmployeeForm(instance=employee)
    context={"form":form}

    if request.method=="POST":        
        form = EmployeeForm(request.POST,instance=employee)
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
