from django import forms
from .models import InputDevices, MqttServers,InputAddresses

class InputDeviceForm(forms.ModelForm):
    
    class Meta:
         model=InputDevices
         fields={'device_name','ip_address','port','device_protocol'}


class InputAddressForm(forms.ModelForm):
    
    class Meta:
         model=InputAddresses
         fields={'variable_name','address','device'}

class MqttServerForm(forms.ModelForm):
    
    class Meta:
         model=MqttServers
         fields={'device_name','ip_address','port','mqtt_user_name','mqtt_password'}


