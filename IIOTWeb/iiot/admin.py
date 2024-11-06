from django.contrib import admin
from .models import InputAddresses
from .models import InputDevices
from .models import MqttServers

admin.site.register(InputAddresses)
admin.site.register(InputDevices)
admin.site.register(MqttServers)

# Register your models here.
