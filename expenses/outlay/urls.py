from django.urls import path
from . import views

app_name='outlay'

urlpatterns = [
    path('',views.index, name='index'),
    path('add-outlay', views.add_outlay, name='add_outlay'),
] 
