from django.shortcuts import render

# Create your views here.
def index(request):
    return render(request,'outlay/index.html')

def add_outlay(request):
    return render(request,'outlay/add_outlay.html')