from django import forms
from .models import InputDevice, MqttServer,InputAddress

class InputDeviceForm(forms.ModelForm):
    
    class Meta:
         model=InputDevice
         fields={'device_name','ip_address','port','device_protocol'}


class InputAddressForm(forms.ModelForm):
    
    class Meta:
         model=InputAddress
         fields={'variable_name','address','device_id'}

class MqttServerForm(forms.ModelForm):
    
    class Meta:
         model=MqttServer
         fields={'device_name','ip_address','port','mqtt_user_name','mqtt_password'}


