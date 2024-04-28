from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from controller.models import *
from controller.funs import *
from api.models import *

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
        })
    return JsonResponse(response)

def genTopo(request):
    topoInfo = analyze_routing_topology()
    try:
        response = {}
        for srcIP, dstIP, next_hop, interface in topoInfo:
            if response.get(srcIP) is None:
                response[srcIP] = []
            response[srcIP].append({
                'next_hop': next_hop,
                'dstIP': dstIP,  #用于转发表，建立拓扑可以不用用到这个字段
                'interface': interface
            })
        return JsonResponse(response)
    except Exception as e:
        print("error!!!",str(e))
        return HttpResponse(type(e).__name__+" "+str(e),status=500)

def FIB(request):
    fib = analyze_fib()
    try:
        response = {}
        for i, (node, entries)in enumerate(fib.items()):
            if response.get(node) is None:
                response[node] = []
            device = deviceModel.objects.get(id= i + 1)
            for entry in entries:
                # 存入数据库操作，注意这里是更新覆盖的
                FIB_Model.objects.update_or_create(
                    deviceId_id=device.id,
                    dstIP=entry['dstIP'],
                    outInterfaceId=entry['outInterfaceId']
                )
                response[node].append({
                    'dstIP': entry['dstIP'],
                    'outInterfaceId': entry['outInterfaceId']
                })
        return JsonResponse(response)
    except Exception as e:
        return HttpResponse(f"Internal Server Error: {str(e)}", status=500)

def verifyTable(request):
    vt = analyze_vt()
    try:
        response = {}
        #enumerate(vt.items())
        for i, (node, entries) in enumerate(vt.items()):
            if response.get(node) is None:
                response[node] = []
            device = deviceModel.objects.get(id = i+1)
            for entry in entries:
                #存入数据库操作，注意这里是更新覆盖的
                verifyTable_Model.objects.update_or_create(
                    deviceId_id=device.id,
                    srcIP=entry['srcIP'],
                    inInterfaceId=entry['inInterfaceId']
                )
                response[node].append({
                    'srcIP': entry['srcIP'],
                    'inInterfaceId': entry['inInterfaceId']
                })
        return JsonResponse(response)
    except Exception as e:
        return HttpResponse(f"Internal Server Error: {str(e)}", status=500)


# 拓扑链路信息
def topoLink(request):
    link_performance = analyze_link_performance()
    try:
        response = {}
        for (srcIP, dstIP, next_hop, interface), performance in link_performance.items():
            if srcIP not in response:
                response[srcIP] = []
            response[srcIP].append({
                'srcIP': srcIP,
                'next_hop': next_hop,
                'link_performance': performance
            })
        return JsonResponse(response)
    except Exception as e:
        print("error!!!", str(e))
        return HttpResponse(f"{type(e).__name__} {str(e)}", status=500)


def topoNode(request):
    node_performance = analyze_node_performance()
    try:
        response = {}
        for node, performance in node_performance.items():
            response[node] = {
                'node': node,
                'node_performance': performance
            }
        return JsonResponse(response)
    except Exception as e:
        print("error!!!", str(e))
        return HttpResponse(f"{type(e).__name__} {str(e)}", status=500)

def showController(request):
    rib = RIB_Model.objects.all()
    response = [{'ribLen': len(rib), 'pathNum': 1, 'deviceNum': 4}]
    return JsonResponse(response, safe=False)