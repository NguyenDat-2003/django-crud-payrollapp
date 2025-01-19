from django.urls import path

from LegacyDatabasesApp import views

urlpatterns = [
  path("ShowCategories/", views.ShowCategories,name="ShowCategories"),
  path("RawSqlDemo", views.RawSqlDemo,name="RawSqlDemo"),
  path("StoredProcedureDemo", views.StoredProcedureDemo,name="StoredProcedureDemo"),
  path("SPWithParametersDemo", views.SPWithParametersDemo,name="SPWithParametersDemo"),
  path('FilteringQuerySetsDemo', views.FilteringQuerySetsDemo,name='FilteringQuerySetsDemo'),
]
