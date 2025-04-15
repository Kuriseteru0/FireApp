from django.shortcuts import render
from django.http import JsonResponse
from .models import FireIncident  # Ensure you have a model for fire incidents

def map_fire_incidents(request):
    if request.method == "GET" and "city" in request.GET:
        city = request.GET.get("city")
        incidents = FireIncident.objects.filter(city__iexact=city)
    else:
        incidents = FireIncident.objects.all()

    data = [
        {
            "id": incident.id,
            "latitude": incident.latitude,
            "longitude": incident.longitude,
            "city": incident.city,
            "severity": incident.severity,
        }
        for incident in incidents
    ]
    return JsonResponse(data, safe=False)