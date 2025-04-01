# forms.py
from django import forms
from .models import InputDevices, MqttServers, InputAddresses, InfluxDatabases, InfluxMeasurement

# Model form for Input Devices


class InputDeviceForm(forms.ModelForm):
    class Meta:
        model = InputDevices
        fields = {'device_name', 'ip_address',
                  'port', 'device_protocol', 'rack', 'slot'}


# Model form for Input Addresses
class InputAddressForm(forms.ModelForm):
    class Meta:
        model = InputAddresses
        fields = {'variable_name', 'address', 'device'}


# Model form for MQTT Servers
class MqttServerForm(forms.ModelForm):
    class Meta:
        model = MqttServers
        fields = {'device_name', 'ip_address', 'port',
                  'mqtt_user_name', 'mqtt_password', 'topic'}


# Model form for Influx Databases
class InfluxServerForm(forms.ModelForm):
    class Meta:
        model = InfluxDatabases
        fields = {'device_name', 'ip_address', 'port', 'database', 'duration'}


# Model form for Influx Measurements
class InfluxMeasurementForm(forms.ModelForm):
    class Meta:
        model = InfluxMeasurement
        fields = {'measurement_name', 'data', 'database'}


# Form to create a new Influx Database
class InfluxDBForm(forms.Form):
    db_name = forms.CharField(label='Database Name', max_length=100)


# Form for Pi information, including hostname and IP address
class PiInfoForm(forms.Form):
    pi_name = forms.CharField(label='Machine Name', max_length=20)
    pi_ip_address = forms.GenericIPAddressField(
        label='Machine Address', max_length=24)
    # pi_password=forms.CharField(label='Pi Password', max_length=20, widget=forms.PasswordInput)


# # Form for selecting and connecting to a Wi-Fi network
# class PiWifiForm(forms.Form):
#     wifi_name = forms.ChoiceField(choices=[], label="Select WiFi")
#     wifi_password = forms.CharField(
#         label='WiFi Password', max_length=20, widget=forms.PasswordInput)

#     def __init__(self, *args, **kwargs):
#         wifi_names = kwargs.pop('wifi_names', [])
#         super().__init__(*args, **kwargs)
#         # Dynamically set the choices for the wifi_name field
#         self.fields['wifi_name'].choices = [
#             (wifi, wifi) for wifi in wifi_names]

class PiWifiForm(forms.Form):
    wifi_name = forms.ChoiceField(choices=[], label="Select Wifi")
    wifi_password = forms.CharField(
        label='Wifi Password', max_length=20, widget=forms.PasswordInput)

    def __init__(self, *args, **kwargs):
        # Use 'pop' to retrieve 'wifiNames' from kwargs
        wifi_names = kwargs.pop('wifiNames', [])
        super(PiWifiForm, self).__init__(*args, **kwargs)
        # Dynamically set the choices for the wifi_name field
        self.fields['wifi_name'].choices = [
            (wifi, wifi) for wifi in wifi_names]


# Form to create a measurement in a selected Influx Database
class CreateMeasurementForm(forms.Form):
    database_name = forms.ChoiceField(
        choices=[], label="Select Database")  # Dynamically set choices
    measurement_name = forms.CharField(
        max_length=255, label="Measurement Name")
    field_name = forms.CharField(
        max_length=255, required=False, label="Field Name")
    field_value = forms.IntegerField(
        required=False, initial=1, label="Field Value")

    def __init__(self, *args, **kwargs):
        databases = kwargs.pop('databases', [])
        super().__init__(*args, **kwargs)
        # Dynamically set the choices for the database_name field
        self.fields['database_name'].choices = [(db, db) for db in databases]
