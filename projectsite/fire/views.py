from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic.list import ListView
from fire.models import Locations, Incident, FireStation
from django.db import connection
from django.http import JsonResponse
from django.db.models.functions import ExtractMonth
from django.contrib import messages

from django.db.models import Count
from datetime import datetime


class HomePageView(ListView):
    model = Locations
    context_object_name = 'home'
    template_name = "home.html"

class ChartView(ListView):
    template_name = 'chart.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context

    def get_queryset(self, *args, **kwargs):
        pass

def PieCountbySeverity(request):
    query = '''
    SELECT severity_level, COUNT(*) as count 
    FROM fire_incident
    GROUP BY severity_level
    '''
    data = {}
    with connection.cursor() as cursor:
        cursor.execute(query)
        rows = cursor.fetchall()
        if rows:
            # Construct the dictionary with severity level as keys and count as values 
            data = {severity: count for severity, count in rows}
        else:
            data = {}

    return JsonResponse(data)

def LineCountByMonth(request):
    current_year = datetime.now().year
    result = {month: 0 for month in range(1, 13)}

    incidents_per_month = Incident.objects.filter(date_time__year=current_year).values_list('date_time', flat=True)

    # Counting the number of incidents per month
    for date_time in incidents_per_month:
        month = date_time.month
        result[month] += 1

    # Mapping month numbers to month names
    month_names = {
        1: 'Jan', 2: 'Feb', 3: 'Mar', 4: 'Apr', 5: 'May', 6: 'Jun',
        7: 'Jul', 8: 'Aug', 9: 'Sep', 10: 'Oct', 11: 'Nov', 12: 'Dec'
    }

    result_with_month_names = {month_names[month]: count for month, count in result.items()}

    return JsonResponse(result_with_month_names)

def MultilineIncidentTop3City(request):
    query = '''
        SELECT 
            fl.city, 
            strftime('%m', fi.date_time) AS month, 
            COUNT(fi.id) AS incident_count
        FROM 
            fire_incident fi
        JOIN 
            fire_locations fl ON fi.location_id = fl.id
        WHERE 
            fl.city IN (
                SELECT 
                    fl_top.city
                FROM 
                    fire_incident fi_top
                JOIN 
                    fire_locations fl_top ON fi_top.location_id = fl_top.id
                WHERE 
                    strftime('%Y', fi_top.date_time) = strftime('%Y', 'now')
                GROUP BY 
                    fl_top.city
                ORDER BY 
                    COUNT(fi_top.id) DESC
                LIMIT 3
            )
            AND strftime('%Y', fi.date_time) = strftime('%Y', 'now')
        GROUP BY 
            fl.city, month
        ORDER BY 
            fl.city, month;
    '''

    with connection.cursor() as cursor:
        cursor.execute(query)
        rows = cursor.fetchall()

    result = {}
    months = set(str(i).zfill(2) for i in range(1, 13))

    for row in rows:
        city = row[0]
        month = row[1]
        total_incidents = row[2]

        if city not in result:
            result[city] = {month: 0 for month in months}
        result[city][month] = total_incidents

    while len(result) < 3:
        missing_city = f"City {len(result) + 1}"
        result[missing_city] = {month: 0 for month in months}

    for city in result:
        result[city] = dict(sorted(result[city].items()))

    return JsonResponse(result)

def multipleBarbySeverity(request):
    query = '''
        SELECT
            fi.severity_level,
            strftime('%m', fi.date_time) AS month, 
            COUNT(fi.id) AS incident_count
        FROM 
            fire_incident fi
        GROUP BY fi.severity_level, month
        '''

    with connection.cursor() as cursor:
        cursor.execute(query)
        rows = cursor.fetchall()

    result = {}
    months = set(str(i).zfill(2) for i in range(1, 13))

    # Loop through the query results
    for row in rows:
        level = str(row[0])  # Ensure the severity level is a string
        month = row[1]
        total_incidents = row[2]

        if level not in result:
            result[level] = {month: 0 for month in months}
        
        result[level][month] = total_incidents

    # Sort months within each severity level
    for level in result:
        result[level] = dict(sorted(result[level].items()))

    return JsonResponse(result)


def map_station(request):
    stations = FireStation.objects.all()  # Query all stations
    # Create a list for markers with float coordinates
    fireStations_list = [{
        'name': station.name,
        'latitude': float(station.latitude),
        'longitude': float(station.longitude),
    } for station in stations]

    context = {
        'fireStations': fireStations_list,  # used for displaying markers on the map
        'stations': stations,                # used to populate select boxes for edit and delete
    }
    return render(request, 'map_station.html', context)

def map_incidents(request):
    incidents = Incident.objects.select_related('location').values(
        'id', 'location__latitude', 'location__longitude', 'description'
    )
    # Convert coordinates to float for Leaflet
    for incident in incidents:
        incident['latitude'] = float(incident['location__latitude'])
        incident['longitude'] = float(incident['location__longitude'])
    incidents_list = list(incidents)
    context = {
        'fireIncidents': incidents_list,
    }
    return render(request, 'incidents_map.html', context)

def add_station(request):
    if request.method == 'POST':
        station_name = request.POST.get('name')
        latitude = request.POST.get('latitude')
        longitude = request.POST.get('longitude')
        try:
            latitude = float(latitude)
            longitude = float(longitude)
            new_station = FireStation(name=station_name, latitude=latitude, longitude=longitude)
            new_station.save()
            messages.success(request, "Station added successfully!")
        except Exception as e:
            messages.error(request, "Error adding station: " + str(e))
        return redirect('map_station')
    return redirect('map_station')

def edit_station(request):
    if request.method == 'POST':
        station_id = request.POST.get('station_id')
        station = get_object_or_404(FireStation, id=station_id)
        new_name = request.POST.get('new_name')
        new_latitude = request.POST.get('new_latitude')
        new_longitude = request.POST.get('new_longitude')
        try:
            if new_name:
                station.name = new_name
            if new_latitude:
                station.latitude = float(new_latitude)
            if new_longitude:
                station.longitude = float(new_longitude)
            station.save()
            messages.info(request, "Station updated successfully!")
        except Exception as e:
            messages.error(request, "Error updating station: " + str(e))
        return redirect('map_station')
    return redirect('map_station')

def delete_station(request):
    if request.method == 'POST':
        station_id = request.POST.get('station_id')
        try:
            station = FireStation.objects.get(id=station_id)
            station.delete()
            messages.error(request, "Station deleted successfully!")
        except FireStation.DoesNotExist:
            messages.error(request, "Station not found!")
        return redirect('map_station')
    return redirect('map_station')

