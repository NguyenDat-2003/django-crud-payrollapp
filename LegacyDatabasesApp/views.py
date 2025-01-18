from django.shortcuts import render

from LegacyDatabasesApp.models import Categories

# Create your views here.
def ShowCategories(request):
  categories=Categories.objects.all()      
  return render(request,"LegacyDatabasesApp/ShowCategories.html",{"Categories":categories})
