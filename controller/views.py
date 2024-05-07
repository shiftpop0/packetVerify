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
        # 临时展示，控制3条路由表
        if len(response)> 2:
            break
    return JsonResponse(response)

def genTopo(request):
    topoInfo = analyze_routing_topology()
    try:
        response = []
        for deviceID, srcIP, dstIP, next_hop, inInterface, outInterface in topoInfo:
            response.append({
                'deviceId': deviceID,
                'srcIP': srcIP,
                'dstIP': dstIP,
                'next_hop': next_hop,
                'inInterface': inInterface,
                'outInterface': outInterface
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
    rib = RIB_Model.objects.all()
    response = [{'ribLen': len(rib), 'pathNum': 1, 'deviceNum': 4}]
    return JsonResponse(response, safe=False)