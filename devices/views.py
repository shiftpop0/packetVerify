import requests
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render
import json


def showDevice(request):
    device_url = 'http://127.0.0.1:8001/device'
    deviceInfo = json.loads(requests.get(device_url+'/deviceInfo').text).get('data')
    netInfo = json.loads(requests.get(device_url+'/netInfo').text).get('data')
    response = []
    response.append({'deviceId': 0, 'deviceInfo': deviceInfo, 'netInfo': netInfo})
    print(response)
    return JsonResponse(response, safe=False)