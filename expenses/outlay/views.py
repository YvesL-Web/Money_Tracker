from django.db.models import Sum
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.paginator import Paginator
from django.http import JsonResponse

import plotly.express as px
import json
import datetime
from .forms import FilterDate
from .models import Category, Outlay
from userpreferences.models import UserPreference

# Create your views here.
@login_required(login_url='users:login')
def index(request):
    categories = Category.objects.all()
    outlays = Outlay.objects.filter(user=request.user)
    paginator = Paginator(outlays,10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    currency = UserPreference.objects.get(user=request.user).currency
    context={
        'categories': categories,
        'outlays': outlays,
        'pages': page_obj,
        'currency': currency,
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
    
def outlay_summary(request):
    today_date = datetime.date.today()
    six_month_ago = today_date - datetime.timedelta(days=30*6)
    outlays = Outlay.objects.filter(date__gte=six_month_ago,date__lte=today_date, user=request.user )
    data={}

    def get_category(outlay):
        return outlay.category
    
    category_list = list(set(map(get_category, outlays)))

    def get_category_amount(category):
        amount=0
        filtered_by_category = outlays.filter(category=category)

        for item in filtered_by_category:
            amount += item.amount

        return amount


    for outlay in outlays:
        for category in category_list:
            data[category]=get_category_amount(category)

    return JsonResponse({'outlay_category_data': data}, safe=False)

def stats_view(request):
    return render(request, 'outlay/stats.html')



def chart(request):
    cat_sum = Outlay.objects.values('category').annotate(total_exp=Sum('amount',distinct=True)).filter(user=request.user)
    start= request.GET.get('start')
    end= request.GET.get('end')
    

    if start:
        cat_sum = cat_sum.filter(date__gte=start)
    if end:
        cat_sum = cat_sum.filter(date__lte=end)

    
    x= list(cat_sum.values_list('category',flat=True))
    y= list(cat_sum.values_list('total_exp',flat=True))
    text= [f"{sum:.0f}" for sum in y ]

    fig = px.bar(
        x=x,
        y=y,
        text=text,
        title= 'Summary',
        labels={'x':'Category', 'y':'expenses'}
    )
    fig.update_layout(title={
        'font_size':22,
        'xanchor':'center',
        'x':0.5
    })
    fig.update_traces(textfont_size=12, textangle=0)


    chart = fig.to_html()
    context = {'chart': chart, 'form':FilterDate, 'cat':list(x) , 'total':list(y)}
    return render(request, 'outlay/stats.html', context)