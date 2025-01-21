from django import template
from django.shortcuts import render
from LegacyDatabasesApp.models import OrderDetails, Orders

register = template.Library() 

@register.inclusion_tag('LegacyDatabasesApp/OrdersWithAccordion_CTT.html')
def show_orders(start=10248,end=10255):
  orders = Orders.objects.filter(orderid__range=[start,end]).order_by('orderid')
  listOrderIds = [ order.orderid for order in orders ]

  listOrderDetails = OrderDetails.objects.filter(orderid__in=listOrderIds).order_by('orderid')

  context = {      
        'orders': orders,
        'order_details': listOrderDetails        
    }
  return (context)

@register.simple_tag(name="calculate_billamount")
def calculate_billamount(quantity,unitprice):    
  return (quantity * unitprice)
