from django import forms
from .models import InputDevices, MqttServers,InputAddresses

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


class InfluxDBForm(forms.Form):
    db_name = forms.CharField(label='Database Name', max_length=100)


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


