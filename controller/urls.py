from django.contrib import admin
from django.urls import path
from controller.views import *

urlpatterns = [
    path("index",index),  #没用到
    path("registe", registe), #没用到
    path("genTopo", genTopo), #生成拓扑
    path("rib", RIB), #路由表
    path("fib", FIB), #转发表
    path("verifyTable", verifyTable),#验证表
    path("topoLink", topoLink), #拓扑链路信息
    path("topoNode", topoNode), #拓扑节点（主机）信息
    path("showController", showController), #显示控制器信息"
    path('delete_rib', delete_rib_entries), #删除路由表
    path("update_rib", update_rib_entries), #更新路由表
]