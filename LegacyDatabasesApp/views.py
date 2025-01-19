from django.shortcuts import render
import pyodbc
from django.db.models import Q,Avg,Max,Min,Sum,Count


from LegacyDatabasesApp.models import Categories, Orders

# Create your views here.
def ShowCategories(request):
  categories=Categories.objects.all()      
  return render(request,"LegacyDatabasesApp/ShowCategories.html",{"Categories":categories})

def GetConnection():
  cnxn = pyodbc.connect('DRIVER=ODBC Driver 17 for SQL Server;Server=.;Database=Northwind;Trusted_Connection=Yes;')
  return(cnxn)

def RawSqlDemo(request):
  query='''
      SELECT a.OrderID,a.OrderDate,b.CompanyName,
      c.ProductName,d.UnitPrice,d.Quantity,
      d.unitprice * d.Quantity as 'BillAmount'
      from orders a inner join [order details] d on a.orderid=d.orderid inner join
      customers b on a.customerid=b.customerid inner join
      products c on d.productid=c.productid
      where a.orderid between 10248 and 10255
      '''
  cnxn= GetConnection()
  cursor = cnxn.cursor()    
  cursor.execute(query)
  orders=cursor.fetchall()
  cursor.close()
  cnxn.close()
  return render(request,"LegacyDatabasesApp/ShowOrders.html",{"Orders":orders})


def StoredProcedureDemo(request):
  cnxn= GetConnection()
  cursor = cnxn.cursor()    
  cursor.execute("{call SP_GetAllOrders}")
  orders=cursor.fetchall()
  cursor.close()
  cnxn.close()
  return render(request,"LegacyDatabasesApp/ShowOrders.html",{"Orders":orders})

def SPWithParametersDemo(request):
  cnxn= GetConnection()
  cursor = cnxn.cursor()   
  count = 0 
  cursor.execute("{call SP_GetOrdersCount(?)}",count)
  count=cursor.fetchval()

  cursor.execute("{call SP_GetAllOrders}")
  orders=cursor.fetchall()

  subtotal = 0
  runningTotal = 0
  runningOrderTotal = 0
  runningOrderTotal = 0
  newOrders = []

  prevOrderId = 0

  for order in orders:
    if prevOrderId == 0:
      prevOrderId = order.OrderID
      runningTotal += order.BillAmount
      runningOrderTotal += order.BillAmount
      subtotal += order.BillAmount
      newOrders.append(pushData(order,runningTotal,runningOrderTotal))
    elif prevOrderId == order.OrderID:
      runningTotal += order.BillAmount
      runningOrderTotal += order.BillAmount
      subtotal += order.BillAmount
      newOrders.append(pushData(order,runningTotal,runningOrderTotal))
    else :
      newOrders.append(pushData(0,subtotal,0))
      prevOrderId = order.OrderID
      runningTotal += order.BillAmount
      runningOrderTotal += order.BillAmount
      subtotal += order.BillAmount
      newOrders.append(pushData(order,runningTotal,runningOrderTotal))

  newOrders.append(pushData(0,subtotal,0))

  cursor.close()
  cnxn.close()
  return render(request,"LegacyDatabasesApp/ShowOrders.html",{"Orders":newOrders ,"Count":count , "GrandTotal":runningTotal})

def pushData(order,runningTotal,runningOrderTotal):
  dataToPush={
            "OrderID": ''  if(order == 0) else order.OrderID,
            "OrderDate":  ''  if(order == 0) else order.OrderDate,
            "CompanyName":  ''  if(order == 0) else order.CompanyName,
            "ProductName":  ''  if(order == 0) else order.ProductName,
            "UnitPrice":  ''  if(order == 0) else order.UnitPrice,
            "Quantity":  ''  if(order == 0) else order.Quantity,
            "BillAmount":  ''  if(order == 0) else order.BillAmount,
            "RunningTotal":runningTotal,
            "RunningOrderTotal":  ''  if(order == 0) else runningOrderTotal,
        }
  return dataToPush

def FilteringQuerySetsDemo(request):
    #orders=Orders.objects.all()

    #orders = Orders.objects.filter(freight__gt=20)
    #orders = Orders.objects.filter(freight__gte=20)   
    #orders = Orders.objects.filter(freight__lt=20)
    #orders = Orders.objects.filter(freight__lte=20)

    #orders = Orders.objects.filter(shipcountry__exact='Germany')

    #orders = Orders.objects.filter(shipcountry__contains='land')

    #orders = Orders.objects.filter(orderid__exact=10248)

    #orders = Orders.objects.filter(employeeid__in=[1,3,5])

    #orders = Orders.objects.filter(employeeid__in=[1,3,5]).order_by('employeeid')
    #orders = Orders.objects.filter(employeeid__in=[1,3,5]).order_by('-employeeid')

    #orders = Orders.objects.filter(shipname__startswith='A')

    #orders = Orders.objects.filter(shipname__endswith='e')

    #orders = Orders.objects.filter(freight__range=[10,20])

    #orders = Orders.objects.filter(shipname__startswith='A') | Orders.objects.filter(freight__lt=20)

    #orders = Orders.objects.filter(Q(shipname__startswith='S') | Q(freight__lt=20))

    #orders = Orders.objects.filter(shipname__startswith='S') & Orders.objects.filter(freight__gte=15)

    #orders = Orders.objects.filter(Q(shipname__startswith='S') & Q(freight__gte=15))

    #orders = Orders.objects.filter(shipname__startswith='A',freight__gte=20)

    #orders = Orders.objects.exclude(shipname__startswith='S')
    #orders = Orders.objects.filter(~Q(shipname__startswith='S'))

    #orders = Orders.objects.all().order_by('orderid')
    #orders = Orders.objects.all().order_by('-orderid')
    #orders = Orders.objects.all().order_by('shipcountry')

    year=1997
    orders=Orders.objects.filter(orderdate__year=year).order_by("-orderdate", "employeeid")

    avg = Orders.objects.all().aggregate(Avg('freight'))
    max = Orders.objects.all().aggregate(Max('freight'))
    min = Orders.objects.all().aggregate(Min('freight'))
    sum = Orders.objects.all().aggregate(Sum('freight'))
    count = Orders.objects.all().aggregate(Count('freight'))

    my_dict = {"Orders":orders,'avg':avg['freight__avg'], 
               'max':max['freight__max'], 
               'min':min['freight__min'],
               'sum':sum['freight__sum'],
               'count':count['freight__count']}    
    
    return render(request,"LegacyDatabasesApp/FilteringDemo.html",
                   {"Orders":my_dict})
