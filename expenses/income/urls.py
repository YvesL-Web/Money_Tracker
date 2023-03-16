from django.urls import path
from django.views.decorators.csrf import csrf_exempt
from . import views

app_name='income'

urlpatterns = [
    path('',views.index, name='index'),
    path('add-income', views.add_income, name='add_income'),
    path('edit-income/<int:pk>', views.income_edit, name='edit_income'),
    path('delete-income/<int:pk>',views.delete_income, name='delete_income'),
    path('search-param',csrf_exempt(views.search_param), name='search_param'),
    path('summary-income',views.summary_income, name='summary_income'),
] 
