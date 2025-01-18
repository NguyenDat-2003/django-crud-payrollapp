from django.shortcuts import render
import pyodbc

from LegacyDatabasesApp.models import Categories

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

