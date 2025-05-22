from django.forms import ModelForm
from django import forms
from .models import Locations, Incident

class LocationForm(ModelForm):
    class Meta:
        model = Locations
        fields = "__all__"

class IncidentForm(ModelForm):
    class Meta:
        model = Incident
        fields = "__all__"