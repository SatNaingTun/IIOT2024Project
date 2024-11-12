from django import forms
from .models import InputDevices, MqttServers,InputAddresses,InfluxDatabases,InfluxMeasurement

class InputDeviceForm(forms.ModelForm):
    
    class Meta:
         model=InputDevices
         fields={'device_name','ip_address','port','device_protocol','rack','slot'}


class InputAddressForm(forms.ModelForm):
    
    class Meta:
         model=InputAddresses
         fields={'variable_name','address','device'}

class MqttServerForm(forms.ModelForm):
    
    class Meta:
         model=MqttServers
         fields={'device_name','ip_address','port','mqtt_user_name','mqtt_password','topic'}


class InfluxServerForm(forms.ModelForm):
    
    class Meta:
         model=InfluxDatabases
         fields={'device_name','ip_address','port','database'}


class InfluxMeasurementForm(forms.ModelForm):
    
    class Meta:
         model=InfluxMeasurement
         fields={'measurement_name','data','database'}


class InfluxDBForm(forms.Form):
    db_name = forms.CharField(label='Database Name', max_length=100)

class PiInfoForm(forms.Form):
    pi_name=forms.CharField(label='Pi Name', max_length=20)
    pi_ip_address=forms.GenericIPAddressField(label='Pi Address',max_length=24)
   
    
   

class PiWifiForm(forms.Form):
    wifi_name = forms.ChoiceField(choices=[], label="Select Wifi")
    wifi_password=forms.CharField(label='Wifi Password', max_length=20)
    
    def __init__(self, *args, **kwargs):
        wifiNames = kwargs.pop('wifiNames', [])
        super().__init__(*args, **kwargs)
        # Dynamically set the choices for the database_name field
        self.fields['wifi_name'].choices = [(wifi, wifi) for wifi in wifiNames]


class CreateMeasurementForm(forms.Form):
    database_name = forms.ChoiceField(choices=[], label="Select Database")  # Set choices dynamically
    measurement_name = forms.CharField(max_length=255, label="Measurement Name")
    field_name = forms.CharField(max_length=255, required=False, label="Field Name")
    field_value = forms.IntegerField(required=False, initial=1, label="Field Value")

    def __init__(self, *args, **kwargs):
        databases = kwargs.pop('databases', [])
        super().__init__(*args, **kwargs)
        # Dynamically set the choices for the database_name field
        self.fields['database_name'].choices = [(db, db) for db in databases]


