from django import forms

class PLCAddressForm(forms.Form):
    variable_name = forms.CharField(label='Variable Name', max_length=24)
    address=forms.CharField(label='PLC Address', max_length=24)