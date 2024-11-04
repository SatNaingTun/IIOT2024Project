# plc_app/forms.py

from django import forms

class PLCAddressForm(forms.Form):
    address = forms.CharField(label='PLC Address', max_length=100)
    variable_name = forms.CharField(label='Variable Name', max_length=100)
