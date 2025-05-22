from django.forms import ModelForm
from django import forms
from .models import Locations, Incident, FireStation, Firefighters

class LocationForm(ModelForm):
    class Meta:
        model = Locations
        fields = "__all__"

class IncidentForm(ModelForm):
    class Meta:
        model = Incident
        fields = "__all__"

class FireStationForm(ModelForm):
    class Meta:
        model = FireStation
        fields = "__all__"

class FirefightersForm(ModelForm):
    class Meta:
        model = Firefighters
        fields = "__all__"