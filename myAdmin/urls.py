from django.contrib import admin
from django.urls import path
from myAdmin.views import *

urlpatterns = [
    path("index",index),
    path("login",login),
    path("admin_index",admin_index),
    path("device_manage", device_manage),
    path("control_manage", controller_manage),  # controller管理
    path("topo_index", topo_index),  # 左侧功能键 拓扑
    path("topo", topo),
    path("ribHtml", ribHtml),
    path("cpuLine", cpuLine),
]