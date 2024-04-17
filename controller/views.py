from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from controller.models import *


def index(request):
    response = HttpResponse("Hello, world. You're at the index.")
    return response

def registe(request):
    return HttpResponse("registe success")

def RIB(request):
    rib = RIB_Model.objects.all()
    response = {}
    for r in rib:
        if response.get(r.deviceId.id) is None:
            response[r.deviceId.id] = []
        response[r.deviceId.id].append({
            'dstIP': r.dstIP,
            'nextHop': r.nextHop,
            'interfaceId': r.interfaceId
        })
    return JsonResponse(response)

def FIB(request):
    fib = FIB_Model.objects.all()
    response = {}
    try:
        for f in fib:
            if response.get(f.deviceId.id) is None:
                response[f.deviceId.id] = []
            response[f.deviceId.id].append({
                'dstIP': f.dstIP,
                'interfaceId': f.interfaceId
            })
    except Exception as e:
        print("error!!!",str(e))
        return HttpResponse(type(e).__name__+" "+str(e),status=500)
    return JsonResponse(response)