from django.forms import ModelForm
from django import forms
from . import models

class InputForm(ModelForm):
    topic=forms.CharField(label="topic", max_length=100)
    address=forms.CharField(label="address", max_length=100)