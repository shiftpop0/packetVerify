from django.contrib import admin
from api.models import *



# Register your models here.
admin.site.register(deviceModel)
admin.site.register(dataPlaneModel)
admin.site.register(controllerModel)
