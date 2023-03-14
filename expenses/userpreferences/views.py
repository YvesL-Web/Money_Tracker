from django.contrib import messages
from django.shortcuts import render
import os
import json
from django.conf import settings

from .models import UserPreference

# Create your views here.
def index(request):

    currency_data = []
    file_path = os.path.join(settings.BASE_DIR, 'currencies.json')
    with open(file_path, "r") as json_file:
        data=json.load(json_file)       
        for k, v in data.items():
            currency_data.append({'name':k, 'value': v})

    exists = UserPreference.objects.filter(user=request.user).exists()
    user_pref = None

    if exists:
       user_pref = UserPreference.objects.get(user=request.user)
    
    
    if request.method == 'POST' :
        currency = request.POST['currency']
        if exists:
            user_pref.currency=currency
            user_pref.save()
            messages.success(request,f'Currency was updated')
            return render(request,'preferences/index.html',{'currencies':currency_data, "user_pref":user_pref})      
        
        UserPreference.objects.create(user=request.user, currency=currency)
        messages.info(request,f'Currency is set to {currency}.')
        return render(request,'preferences/index.html', {'currencies':currency_data, "user_pref":user_pref})
    
    return render(request, 'preferences/index.html', {'currencies':currency_data, "user_pref":user_pref, } )