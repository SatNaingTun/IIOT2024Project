from django import forms
from .models import InputDevice

class InputDeviceForm(forms.ModelForm):
    
    class Meta:
         model=InputDevice
         fields={'device_name','ip_address','port','device_protocol'}

