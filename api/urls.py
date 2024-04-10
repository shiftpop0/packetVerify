from django.contrib import admin
from django.urls import path
from api.views import *

urlpatterns = [
    path("index",index),
    path("verifyIDList",verifyIDList),
    path("deviceInfo",deviceInfo),
    path("dataPlaneInfo",dataPlaneInfo),
    path("controllerInfo",controllerInfo),
]