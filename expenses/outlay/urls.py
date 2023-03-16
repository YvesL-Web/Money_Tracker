from django.urls import path
from django.views.decorators.csrf import csrf_exempt
from . import views

app_name='outlay'

urlpatterns = [
    path('',views.index, name='index'),
    path('add-outlay', views.add_outlay, name='add_outlay'),
    path('edit-outlay/<int:pk>', views.outlay_edit, name='edit_outlay'),
    path('delete-outlay/<int:pk>',views.delete_outlay, name='delete_outlay'),
    path('search-param',csrf_exempt(views.search_param), name='search_param'),
    path('outlay_summary',views.outlay_summary, name='outlay_summary'),
    path('summary',views.chart, name='chart'),
] 
