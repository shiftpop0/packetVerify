from django.contrib import admin
from django.urls import path
from controller.views import *

urlpatterns = [
    path("index",index),
    path("registe", registe),
    path("rib", RIB),
    path("fib", FIB),

]