from django.urls import path
from devices.views import *

urlpatterns = [
    path("showDevice", showDevice),
    path("getPort", getPort),
]