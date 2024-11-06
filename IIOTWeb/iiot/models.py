import uuid
from django.db import models
from .consts import plc_protocols

class InputDevice(models.Model):
    device_id=models.UUIDField(primary_key=True,default=uuid.uuid4,unique=True)
    device_name=models.CharField(max_length=24)
    ip_address=models.GenericIPAddressField(max_length=24)
    port=models.IntegerField()
    device_protocol=models.CharField(max_length=10,choices=plc_protocols,default="S7Tsap")

    def __str__(self):
        return self.device_name

class InputAddress(models.Model):
    address_id=models.UUIDField(primary_key=True,default=uuid.uuid4)
    variable_name=models.CharField(max_length=24)
    address=models.CharField(max_length=24)
    device=models.ForeignKey(InputDevice,on_delete=models.CASCADE)

    # updated_time=models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.variable_name


class MqttServer(models.Model):
    id=models.UUIDField(primary_key=True,default=uuid.uuid4)
    device_name=models.CharField(max_length=24)
    ip_address=models.GenericIPAddressField(max_length=24)
    port=models.IntegerField()
    mqtt_user_name=models.CharField(max_length=24)
    mqtt_password=models.CharField(max_length=24)

    # updated_time=models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.variable_name

