import requests
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render
import json


def showDevice(request):
    device_url = 'http://127.0.0.1:8001/device'
    response = []

    try:
        device_info = json.loads(requests.get(f'{device_url}/deviceInfo').text).get('data')
        for device in device_info:
            response.append({
                'deviceId': device['id'],
                'deviceInfo': {
                    'throughput': device['throughput'],
                    'verifySpeed': device['verifySpeed'],
                    'avgDelay': device['avgDelay'],
                    'verifyMode': device['verifyMode'],
                    'tableUsage': device['tableUsage']
                }
            })
        return JsonResponse(response, safe=False)

    except requests.exceptions.RequestException as e:
        return JsonResponse({'error': 'Failed to fetch device info', 'details': str(e)}, status=500)
    except Exception as e:
        return JsonResponse({'error': 'An error occurred', 'details': str(e)}, status=500)

def getPort(request):
    device_url = 'http://127.0.0.1:8001/device'
    devicePort = json.loads(requests.get(device_url+'/portInfo').text).get('data')
    response = []
    response= {'deviceId': 0, 'devicePort': devicePort}
    print(response)
    return JsonResponse(response, safe=False)


def verifySet(request):
    payload = json.loads(request.body)
    device_id = payload.get('id')

    if device_id is not None:
        device_url = 'http://127.0.0.1:8001/device'
        response = requests.post(device_url + '/verifySwitch', json={'id': device_id})
        response_data = response.json().get('data')
        return JsonResponse(response_data, safe=False)
    else:
        return JsonResponse({'error': 'ID not provided'}, status=400)
