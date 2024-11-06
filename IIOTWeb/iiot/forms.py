from django import forms
from .models import InputDevice, MqttServer

class InputDeviceForm(forms.ModelForm):
    
    class Meta:
         model=InputDevice
         fields={'device_name','ip_address','port','device_protocol'}

class MqttServerForm(forms.ModelForm):
    
    class Meta:
         model=MqttServer
         fields={'device_name','ip_address','port','mqtt_user_name','mqtt_password'}


