import uuid
from django.db import models
from .consts import plc_protocols

class InputDevices(models.Model):
    device_id=models.UUIDField(primary_key=True,default=uuid.uuid4,unique=True)
    device_name=models.CharField(max_length=24)
    ip_address=models.GenericIPAddressField(max_length=24)
    port=models.IntegerField()
    rack=models.IntegerField(default=1)
    slot=models.IntegerField(default=1)
    device_protocol=models.CharField(max_length=10,choices=plc_protocols,default="S7Tsap")

    def __str__(self):
        return self.device_name

class InputAddresses(models.Model):
    address_id=models.UUIDField(primary_key=True,default=uuid.uuid4)
    variable_name=models.CharField(max_length=24)
    address=models.CharField(max_length=24)
    data=models.CharField(max_length=24,default='')
    device=models.ForeignKey(InputDevices,on_delete=models.CASCADE)

    # updated_time=models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.variable_name


class MqttServers(models.Model):
    id=models.UUIDField(primary_key=True,default=uuid.uuid4)
    device_name=models.CharField(max_length=24)
    ip_address=models.GenericIPAddressField(max_length=24)
    port=models.IntegerField()
    topic=models.CharField(max_length=24,default="iiot/data")
    mqtt_user_name=models.CharField(max_length=24)
    mqtt_password=models.CharField(max_length=24)

    # updated_time=models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.device_name
    
class InfluxDatabases(models.Model):
    device_id=models.UUIDField(primary_key=True,default=uuid.uuid4,unique=True)
    device_name=models.CharField(max_length=24)
    ip_address=models.GenericIPAddressField(max_length=24)
    port=models.IntegerField()
    database=models.CharField(max_length=24)
    # user_name=models.CharField(max_length=24)
    # password=models.CharField(max_length=24)

    def __str__(self):
        return self.device_name

  
class InfluxMeasurement(models.Model):
    id=models.UUIDField(primary_key=True,default=uuid.uuid4,unique=True)
    measurement_name=models.CharField(max_length=24)
    data=models.ForeignKey(InputAddresses,on_delete=models.CASCADE)
    database=models.ForeignKey(InfluxDatabases,on_delete=models.CASCADE)

    
    # user_name=models.CharField(max_length=24)
    # password=models.CharField(max_length=24)

    def __str__(self):
        return self.measurement_name
