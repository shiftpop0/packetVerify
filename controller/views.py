from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from controller.models import *
from controller.tests import *
def index(request):
    response = HttpResponse("Hello, world. You're at the index.")
    return response

#TODO 将拓扑信息存入数据库
def genTopo(request):
    topoInfo = analyze_routing_topology()
    try:
        response = {}
        for src, next_hop, interface in topoInfo:
            if response.get(src) is None:
                response[src] = []
            response[src].append({
                'next_hop': next_hop,
                'interface': interface
            })
        return JsonResponse(response)
    except Exception as e:
        print("error!!!",str(e))
        return HttpResponse(type(e).__name__+" "+str(e),status=500)

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

#TODO 存入数据库
def FIB(request):
    fib = analyze_fib()
    try:
        response = {}
        for node, entries in fib.items():
            if response.get(node) is None:
                response[node] = []
            for entry in entries:
                response[node].append({
                    'dstIP': entry['dstIP'],
                    'outInterfaceId': entry['outInterfaceId']
                })
        return JsonResponse(response)
    except Exception as e:
        return HttpResponse(f"Internal Server Error: {str(e)}", status=500)

    # fib = FIB_Model.objects.all()
    # response = {}
    # try:
    #     for f in fib:
    #         if response.get(f.deviceId.id) is None:
    #             response[f.deviceId.id] = []
    #         response[f.deviceId.id].append({
    #             'dstIP': f.dstIP,
    #             'outInterfaceId': f.outInterfaceId
    #         })
    # except Exception as e:
    #     print("error!!!",str(e))
    #     return HttpResponse(type(e).__name__+" "+str(e),status=500)
    # return JsonResponse(response)

#TODO 存入数据库
def verifyTable(request):
    vt = analyze_vt()
    try:
        response = {}
        for node, entries in vt.items():
            if response.get(node) is None:
                response[node] = []
            for entry in entries:
                response[node].append({
                    'srcIP': entry['srcIP'],
                    'inInterfaceId': entry['inInterfaceId']
                })
        return JsonResponse(response)
    except Exception as e:
        return HttpResponse(f"Internal Server Error: {str(e)}", status=500)
    # verify = verifyTable.objects.all()
    # response = {}
    # for v in verify:
    #     if response.get(v.deviceId.id) is None:
    #         response[v.deviceId.id] = []
    #     response[v.deviceId.id].append({
    #         'srcIP': v.srcIP,
    #         'inInterfaceId': v.interfaceId
    #     })
    # return JsonResponse(response)

