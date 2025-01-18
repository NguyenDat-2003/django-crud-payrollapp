from django.urls import path

from LegacyDatabasesApp import views

urlpatterns = [
  path("ShowCategories/", views.ShowCategories,name="ShowCategories"),
]
