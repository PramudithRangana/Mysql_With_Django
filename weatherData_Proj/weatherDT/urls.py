from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),  # Default homepage
    path('weather_station/', views.weather_station, name='Weather-Station'),
    path('weather_alerts/', views.weather_alerts, name='Weather-Alert'),
    path('weather_data/', views.weather_data, name='Weather-Data'),
    path('seasonal_forecasts/', views.seasonal_forecasts, name='Seasonal-Forecast'),
    path('regions/', views.regions, name='Region'),
    path('forecasts/', views.forecasts, name='Forecast'),
    path('forecast_types/', views.forecast_types, name='Forecast-Type'),
    path('forecast_accuracy/', views.forecast_accuracy, name='Forecast-Accuracy'),
    path('accuracy-graph/', views.accuracy_graph_view, name='accuracy_graph'),
]
