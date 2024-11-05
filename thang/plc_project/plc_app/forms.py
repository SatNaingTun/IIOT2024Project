from django import forms

class PLCAddressForm(forms.Form):
    address = forms.CharField(label='PLC Address', max_length=100)
    variable_name = forms.CharField(label='Variable Name', max_length=100)

class MQTTConfigForm(forms.Form):
    mqtt_ip = forms.GenericIPAddressField(label='MQTT Broker IP', required=True)
    mqtt_port = forms.IntegerField(label='MQTT Broker Port', required=True, min_value=1, max_value=65535)
    mqtt_username = forms.CharField(label='MQTT Username', required=False)
    mqtt_client_id = forms.CharField(label='MQTT Client ID', required=True)
    mqtt_topic = forms.CharField(label='MQTT Topic', required=True)

class InfluxDBForm(forms.Form):
    db_name = forms.CharField(label='Database Name', max_length=100)