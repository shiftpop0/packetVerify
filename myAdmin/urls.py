from django.contrib import admin
from django.urls import path
from myAdmin.views import *

urlpatterns = [
    path("index",index),
    path("login",login),
    path("admin_index",admin_index),
    path("device_manage", device_manage),


]