from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.paginator import Paginator
from django.http import JsonResponse

import json

from .models import Category, Outlay

# Create your views here.
@login_required(login_url='users:login')
def index(request):
    categories = Category.objects.all()
    outlays = Outlay.objects.filter(user=request.user)
    paginator = Paginator(outlays,2)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    context={
        'categories': categories,
        'outlays': outlays,
        'pages': page_obj,
    }
    return render(request,'outlay/index.html', context)

@login_required(login_url='users:login')
def add_outlay(request):
    categories = Category.objects.all()
    context = {
        'categories':categories,  
        'values':request.POST
    }

    if request.method == 'POST':
        amount = request.POST['amount']
        description = request.POST['description']
        category = request.POST['category']
        date = request.POST['outlay_date']

        if not amount:
            messages.error(request,'Amount is required!')
            return render(request, 'outlay/add_outlay.html',context)
        
        Outlay.objects.create(user=request.user,amount=amount, category=category, description=description, date=date)
        messages.success(request, "Expenses saved successfully")
        return redirect('outlay:index')


    return render(request,'outlay/add_outlay.html',context)

def outlay_edit(request, pk ):
    outlay = get_object_or_404(Outlay, pk=pk)
    categories = Category.objects.all()
    context = {
        'outlay':outlay,
        'categories':categories
    }
    if request.method == 'POST':
        amount = request.POST['amount']
        description = request.POST['description']
        category = request.POST['category']
        date = request.POST['outlay_date']

        if not amount:
            messages.error(request,'Amount is required!')
            return render(request, 'outlay/edit_outlay.html',context)
        
        
        outlay.user=request.user
        outlay.amount=amount
        outlay.category=category
        outlay.description=description 
        outlay.date=date

        outlay.save()
        messages.success(request, "Expenses updated successfully")
        return redirect('outlay:index')

    return render(request,'outlay/edit_outlay.html', context)

def delete_outlay(request, pk):
    outlay = get_object_or_404(Outlay, pk=pk)
    outlay.delete()
    messages.warning(request, "Your Expenses has been deleted!")
    return redirect('outlay:index')
    
def search_param(request):
    if request.method == 'POST':
        search_str = json.loads(request.body).get('searchText') # transform into a python dict

        outlay = Outlay.objects.filter(
            user=request.user, amount__startswith = search_str
            ) |Outlay.objects.filter(
            user=request.user, category__icontains = search_str
            ) |Outlay.objects.filter(
            user=request.user, description__icontains = search_str
            ) |Outlay.objects.filter(
            user=request.user, date__startswith = search_str
            )
            
        data = outlay.values() # return dictionaries
        return JsonResponse(list(data), safe=False)