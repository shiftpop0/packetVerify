from django.db import models

# Create your models here.
class deviceModel(models.Model):
    prefixCount = models.IntegerField(default=0)
    throughput = models.IntegerField(default=0)
    filterCount = models.IntegerField(default=0)

class dataPlaneModel(models.Model):
    throughput = models.IntegerField(default=0)
    filterCount = models.IntegerField(default=0)
    avgDelay = models.FloatField(default=0)

class controllerModel(models.Model):
    usage = models.FloatField(default=0)
    VPUF = models.FloatField(default=0)
    VPA = models.IntegerField(default=0)
