from django.contrib import admin
from django.urls import path

from fire.views import HomePageView, ChartView, PieCountbySeverity, LineCountByMonth, MultilineIncidentTop3Country, multipleBarbySeverity, map_incidents, LocationList, LocationCreateView, LocationUpdateView, LocationDeleteView, IncidentList, IncidentCreateView, IncidentUpdateView, IncidentDeleteView, FireStationList, FireStationCreateView, FireStationUpdateView, FireStationDeleteView, FirefightersList, FirefightersCreateView, FirefightersUpdateView, FirefightersDeleteView, FireTruckList, FireTruckCreateView, FireTruckUpdateView, FireTruckDeleteView
from fire import views

urlpatterns = [
    path("admin/", admin.site.urls),
    path('', HomePageView.as_view(), name='home'),
    path('dashboard_chart', ChartView.as_view(), name='dashboard_chart'),
    path('pieChart/', PieCountbySeverity, name='chart'),
    path('lineChart/', LineCountByMonth, name='chart'),
    path('multilineChart/', MultilineIncidentTop3Country, name='chart'),
    path('multiBarChart/', multipleBarbySeverity, name='chart'),
    path('stations', views.map_station, name='map_station'),
    path('incidents', map_incidents, name='map_incidents'),
    path('locations/', LocationList.as_view(), name='location-list'),
    path('locations/add/', LocationCreateView.as_view(), name='location-add'),
    path('locations/<pk>/', LocationUpdateView.as_view(), name='location-update'),
    path('locations/<pk>/delete/', LocationDeleteView.as_view(), name='location-delete'),
    path('incidents/', IncidentList.as_view(), name='incident-list'),
    path('incidents/add/', IncidentCreateView.as_view(), name='incident-add'),
    path('incidents/<pk>/', IncidentUpdateView.as_view(), name='incident-update'),
    path('incidents/<pk>/delete/', IncidentDeleteView.as_view(), name='incident-delete'),
    path('firestations/', FireStationList.as_view(), name='firestations-list'),
    path('firestations/add/', FireStationCreateView.as_view(), name='firestations-add'),
    path('firestations/<pk>/', FireStationUpdateView.as_view(), name='firestation-update'),
    path('firestations/<pk>/delete/', FireStationDeleteView.as_view(), name='firestation-delete'),
    path('firefighters/', FirefightersList.as_view(), name='firefighters-list'),
    path('firefighters/add/', FirefightersCreateView.as_view(), name='firefighters-add'),
    path('firefighters/<pk>/', FirefightersUpdateView.as_view(), name='firefighters-update'),
    path('firefighters/<pk>/delete/', FirefightersDeleteView.as_view(), name='firefighters-delete'),
    path('firetrucks/', FireTruckList.as_view(), name='firetrucks-list'),
    path('firetrucks/add/', FireTruckCreateView.as_view(), name='firetrucks-add'),
    path('firetrucks/<pk>/', FireTruckUpdateView.as_view(), name='firetrucks-update'),
    path('firetrucks/<pk>/delete/', FireTruckDeleteView.as_view(), name='firetrucks-delete'),
]