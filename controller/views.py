import json

from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.views.decorators.http import require_http_methods
from controller.models import *
from controller.funs import *
from api.models import *
from .models import RIB_Model, FIB_Model, verifyTable_Model

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
            'srcIP': r.srcIP,
            'dstIP': r.dstIP,
            'nextHop': r.nextHop,
            'inInterfaceId': r.inInterfaceId,
            'outInterfaceId': r.outInterfaceId,
            'controller_ip': r.controller_ip
        })
        # 临时展示，控制3条路由表
        if len(response)> 2:
            break
    return JsonResponse(response)

def genTopo(request):
    topoInfo = analyze_routing_topology()
    try:
        response = []
        for deviceID, srcIP, dstIP, next_hop, inInterface, outInterface, controller_ip in topoInfo:
            response.append({
                'deviceId': deviceID,
                'srcIP': srcIP,
                'dstIP': dstIP,
                'next_hop': next_hop,
                'inInterface': inInterface,
                'outInterface': outInterface,
                'controller_ip':  controller_ip
            })
        return JsonResponse(response, safe=False)
    except Exception as e:
        print("error!!!", str(e))
        return HttpResponse(type(e).__name__ + " " + str(e), status=500)

def FIB(request):
    fib = analyze_fib()
    try:
        response = []
        for node, entries in fib.items():
            device = deviceModel.objects.get(id=int(node))  # 直接使用 node 作为设备ID
            for entry in entries:
                # 存入数据库操作，注意这里是更新覆盖的
                FIB_Model.objects.update_or_create(
                    deviceId_id=device,
                    dstIP=entry['dstIP'],
                    outInterfaceId=entry['outInterface']
                )
                response.append({
                    'deciceID': int(node),
                    'dstIP': entry['dstIP'],
                    'outInterfaceId': entry['outInterface']
                })
        return JsonResponse(response,safe=False)
    except Exception as e:
        return HttpResponse(f"Internal Server Error: {str(e)}", status=500)

def verifyTable(request):
    vt = analyze_vt()
    try:
        response = []
        for node, entries in vt.items():
            device = deviceModel.objects.get(id=int(node))  # 直接使用 node 作为设备ID
            for entry in entries:
                #存入数据库操作，注意这里是更新覆盖的
                verifyTable_Model.objects.update_or_create(
                    deviceId_id=device,
                    srcIP=entry['srcIP'],
                    inInterfaceId=entry['inInterface']
                )
                response.append({
                    'deciceID': int(node),
                    'srcIP': entry['srcIP'],
                    'inInterface': entry['inInterface']
                })
        return JsonResponse(response,safe=False)
    except Exception as e:
        return HttpResponse(f"Internal Server Error: {str(e)}", status=500)


# 拓扑链路信息
def topoLink(request):
    link_performance = analyze_link_performance()
    try:
        response = []  #
        for deviceID, performance in link_performance.items():
            response.append({
                'deviceID': deviceID,
                'link_performance': performance
            })
        return JsonResponse(response, safe=False)
    except Exception as e:
        print("error!!!", str(e))
        return HttpResponse(f"{type(e).__name__} {str(e)}", status=500)

def topoNode(request):
    node_performance = analyze_node_performance()
    try:
        response = []
        for deviceID, performance in node_performance.items():
            response.append( {
                'deviceID': deviceID,
                'node_performance': performance
            })
        return JsonResponse(response, safe=False)
    except Exception as e:
        print("error!!!", str(e))
        return HttpResponse(f"{type(e).__name__} {str(e)}", status=500)

def showController(request):
    rib_count = RIB_Model.objects.count()
    device_count = RIB_Model.objects.values('deviceId').distinct().count()
    path_num = 1
    deviceID = 1 #控制器只有一个只能先这一个
    rib = RIB_Model.objects.all()
    response = [{'deviceId':deviceID, 'ribLen': rib_count, 'pathNum': path_num, 'deviceNum': device_count}]
    return JsonResponse(response, safe=False)


#post请求来删掉RIB表项
@require_http_methods(["POST"])
def delete_rib_entries(request):
    device_id = request.GET.get('device_id') # 注意是从Get请求中提取device_id
    if not device_id:
        return JsonResponse({'status': 'error', 'message': 'Device ID is required'}, status=400)
    RIB_Model.objects.filter(deviceId_id=device_id).delete()
    return JsonResponse({
        'status': 'success'
    })

#post请求修改RIB表项
@require_http_methods(["POST"])
def update_rib_entries(request):
    device_id = request.GET.get('device_id')
    if not device_id:
        return JsonResponse({'status': 'error', 'message': 'Device ID is required'}, status=400)

    try:
        # 打印请求体用于调试
        request_body = request.body.decode('utf-8')
        print(f"Request body: {request_body}")

        data = json.loads(request_body)

        # 验证数据是否包含所有必需的字段
        required_fields = ['srcIP', 'dstIP', 'nextHop', 'inInterfaceId', 'outInterfaceId']
        if not all(field in data for field in required_fields):
            return JsonResponse({'status': 'error', 'message': 'Missing required fields'}, status=400)

        srcIP = data['srcIP']
        dstIP = data['dstIP']
        nextHop = data['nextHop']
        inInterfaceId = data['inInterfaceId']
        outInterfaceId = data['outInterfaceId']

        # 尝试根据 device_id 查找记录
        rib_entry = RIB_Model.objects.filter(deviceId_id=device_id).first()
        if not rib_entry:
            return JsonResponse({'status': 'error', 'message': 'Record not found'}, status=404)

        # 更新记录字段
        rib_entry.srcIP = srcIP
        rib_entry.dstIP = dstIP
        rib_entry.nextHop = nextHop
        rib_entry.inInterfaceId = inInterfaceId
        rib_entry.outInterfaceId = outInterfaceId
        rib_entry.save()

        return JsonResponse({'status': 'success'})
    except json.JSONDecodeError:
        return JsonResponse({'status': 'error', 'message': 'Invalid JSON format'}, status=400)
    except Exception as e:
        return JsonResponse({'status': 'error', 'message': str(e)}, status=400)