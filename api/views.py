import json

from django.http import HttpResponse, JsonResponse
from django.shortcuts import render
import json
from api.models import *


def index(request):
    response = HttpResponse("Hello, world. You're at the polls index.")
    return response

def verifyIDList(request):
    devices = deviceModel.objects.all()
    id_list = [device.id for device in devices]
    return JsonResponse(id_list, safe=False)

def deviceInfo(request):
    try:
        device_id = json.loads(request.body).get('id')
    except Exception as e:
        print("error!!!",str(e))
        return HttpResponse(type(e).__name__+" "+str(e),status=500)
    if device_id is None:
        return HttpResponse("device_id is None",status=500)
    try:
        device = deviceModel.objects.get(id=device_id)
    except Exception as e:
        return HttpResponse(type(e).__name__+" "+str(e),status=500)
    response = {
        'prefixCount': device.prefixCount,
        'throughput': device.throughput,
        'filterCount': device.filterCount
    }
    return JsonResponse(response)

def dataPlaneInfo(request):
    dataPlane = dataPlaneModel.objects.get(id=1)
    response = {
        'throughput': dataPlane.throughput,
        'filterCount': dataPlane.filterCount,
        'avgDelay': "{:.2f}".format(dataPlane.avgDelay)
    }
    return JsonResponse(response)

def controllerInfo(request):
    controller = controllerModel.objects.get(id=1)
    response = {
        'usage': "{:.2f}".format(controller.usage),
        'VPUF': "{:.2f}".format(controller.VPUF),
        'VPA': controller.VPA
    }
    return JsonResponse(response)