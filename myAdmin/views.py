import requests
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render
import json
from myAdmin.models import *

def index(request):
    return render(request, 'index.html')

def login(request):
    return render(request, 'login.html')

def admin_index(request):
    return render(request, 'admin_index.html')

def device_manage(request):
    return render(request, 'device_manage.html')

def topo(request):
    return render(request, 'topo.html')

