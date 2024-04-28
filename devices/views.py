import requests
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render
import json


def showDevice(request):
    device_url = 'http://127.0.0.1:8001/device'
    deviceInfo = json.loads(requests.get(device_url+'/deviceInfo').text).get('data')
    # netInfo = json.loads(requests.get(device_url+'/netInfo').text).get('data')
    response = []
    response.append({'deviceId': 1, 'deviceInfo': deviceInfo})
    # test
    deviceInfo = {"throughput": 200, "verifySpeed": 200, "avgDelay": 0.05, "verifyMode": True, "tableUsage": 0.25}
    response.append({'deviceId': 2, 'deviceInfo': deviceInfo})
    print(response)
    return JsonResponse(response, safe=False)

def getPort(request):
    device_url = 'http://127.0.0.1:8001/device'
    devicePort = json.loads(requests.get(device_url+'/portInfo').text).get('data')
    response = []
    response= {'deviceId': 0, 'devicePort': devicePort}
    print(response)
    return JsonResponse(response, safe=False)

def verifySet(request):
    device_url = 'http://127.0.0.1:8001/device'
    response = json.loads(requests.get(device_url + '/verifySwitch').text).get('data')
    return JsonResponse(response, safe=False)