from django.db import models
# from api.models import *

class RIB_Model(models.Model):
    id=models.AutoField(primary_key=True)
    deviceId = models.ForeignKey('api.deviceModel', on_delete=models.CASCADE)
    dstIP = models.CharField(max_length=17)
    nextHop = models.CharField(max_length=15)
    interfaceId = models.IntegerField()

class FIB_Model(models.Model):
    id = models.AutoField(primary_key=True)
    deviceId = models.ForeignKey('api.deviceModel', on_delete=models.CASCADE)
    dstIP = models.CharField(max_length=17)
    interfaceId = models.CharField(max_length=15)