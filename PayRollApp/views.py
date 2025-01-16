from django.shortcuts import redirect, render
from CRUDOperationsExample import settings
from PayRollApp.forms import EmployeeForm,PartTimeEmployeeForm,PartTimeEmployeeFormSet
from PayRollApp.models import Employee,PartTimeEmployee
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.db.models import Q


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

def BulkEmployeeUpdate(request):
    employees = PartTimeEmployee.objects.all()
    forms = [PartTimeEmployeeForm(request.POST or None, instance=emp , prefix=f"employee-{emp.id}" ) for emp in employees]

    if request.method == "POST":
        updated_data = []
        for form in forms:
            if form.is_valid():
                emp = form.instance
                emp.FirstName = form.cleaned_data['FirstName']
                emp.LastName = form.cleaned_data['LastName']
                emp.TitleName = form.cleaned_data['TitleName']
                updated_data.append(emp)
        PartTimeEmployee.objects.bulk_update(updated_data,fields=["FirstName","LastName","TitleName"])
    
    return render(request,"PayRollApp/BulkUpdate.html",{"forms" : forms})

def BulkDelete(request):
    employees = PartTimeEmployee.objects.all()

    if request.method == "POST":
        selected_ids = request.POST.getlist('selected_ids')

        if selected_ids:
            PartTimeEmployee.objects.filter(pk__in=selected_ids).delete()
            return redirect('BulkDelete')
        
    return render(request,"PayRollApp/BulkDelete.html",{"employees" : employees})

def BulkDeleteUsingRadio(request):
    employees = PartTimeEmployee.objects.all()

    if request.method == "POST":
        selected_id = request.POST.get('selected_id')
        if selected_id:
            PartTimeEmployee.objects.filter(pk=selected_id).delete()
            return redirect('BulkDeleteUsingRadio')
        
    return render(request,"PayRollApp/BulkDeleteUsingRadio.html",{"employees" : employees})

def PageWiseEmployeesList(request):
    per_page = int(request.GET.get('per_page', getattr(settings, 'PER_PAGE')))
    page_number = request.GET.get("page")
    employees_page = PartTimeEmployee.objects.all()

    # ----------------- Search Functionality
    search_query = request.GET.get("search" , "")
    # Query employees based on the search query
    employees_page = PartTimeEmployee.objects.filter(
        Q(id__icontains=search_query) |
        Q(FirstName__icontains=search_query) |
        Q(LastName__icontains=search_query) |
        Q(TitleName__icontains=search_query)
    )

    paginator = Paginator(employees_page, per_page)  

    try:
        employees_page = paginator.page(page_number)
    except PageNotAnInteger:
        # Nếu page_number không thuộc kiểu integer, trả về page đầu tiên
        employees_page = paginator.page(1)
    except EmptyPage:
        # Nếu page không có item nào, trả về page cuối cùng
        employees_page = paginator.page(paginator.num_pages)

    context = { 
        "employees_page" : employees_page, 
        "paginator":paginator ,
        "per_page": per_page,
        "search_query": search_query,
        }

    return render(request,"PayRollApp/PageWiseEmployees.html",context)
