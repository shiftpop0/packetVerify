import requests
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render
import json
from myAdmin.models import *
from controller.views import RIB

def index(request):
    return render(request, 'index.html')

def login(request):
    return render(request, 'login.html')

def admin_index(request):
    return render(request, 'admin_index.html')

def device_manage(request):
    return render(request, 'device_manage.html')

def controller_manage(request):
    return render(request, 'controller_manage.html')

def topo(request):
    return render(request, 'topo.html')

def topo_index(request):
    return render(request, 'topo_index.html')

def ribHtml(request):
    url = 'http://127.0.0.1:8000'
    data = json.loads(requests.get(url+'/controller/rib').text).get('data')
    # data = RIB(request)['data']
    data={'data':data}
    return render(request, 'rib.html', data)

def cpuLine(request):
    return render(request, 'cpuLine.html')


