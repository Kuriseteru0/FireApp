from django.contrib import admin
from django.urls import path

from fire.views import HomePageView, ChartView, PieCountbySeverity, LineCountByMonth, MultilineIncidentTop3City, multipleBarbySeverity, map_incidents, add_station, edit_station, delete_station, add_incident, edit_incident, delete_incident
from fire import views

urlpatterns = [
    path("admin/", admin.site.urls),
    path('', HomePageView.as_view(), name='home'),
    path('dashboard_chart', ChartView.as_view(), name='dashboard_chart'),
    path('pieChart/', PieCountbySeverity, name='chart'),
    path('lineChart/', LineCountByMonth, name='chart'),
    path('multilineChart/', MultilineIncidentTop3City, name='chart'),
    path('multiBarChart/', multipleBarbySeverity, name='chart'),
    path('stations', views.map_station, name='map_station'),
    path('incidents', map_incidents, name='map_incidents'),
    path('add_station', add_station, name='add_station'),
    path('edit_station', edit_station, name='edit_station'),
    path('delete_station', delete_station, name='delete_station'),
    path('add_incident', add_incident, name='add_incident'),
    path('edit_incident', edit_incident, name='edit_incident'),
    path('delete_incident', delete_incident, name='delete_incident'),
]