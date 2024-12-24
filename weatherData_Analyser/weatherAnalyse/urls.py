from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),  # Default homepage
    path('weather_station/', views.weather_station, name='Weather-Station'),
    path('get_new_alert_id/', views.get_new_alert_id, name='get_new_alert_id'),
    path('weather_alerts/', views.weather_alerts, name='Weather-Alert'),
    path('add_weather_alert/', views.add_weather_alert, name='Add-Weather-Alert'),
    path('save_all_weather_alerts/', views.save_all_weather_alerts, name='Save-All-Weather-Alert'),
    path('update_weather_alerts/', views.update_weather_alerts, name='update_weather_alerts'),
    path('delete_weather_alerts/', views.delete_weather_alerts, name='Delete-Weather-Alert'),
    path('weather_data/', views.weather_data, name='Weather-Data'),
    path('seasonal_forecasts/', views.seasonal_forecasts, name='Seasonal-Forecast'),
    path('regions/', views.regions, name='Region'),
    path('get_new_region_id', views.get_new_region_id, name='get_new_region_id'),
    path('save_all_regions/', views.save_all_regions, name='save_all_regions'),
    path('update_regions/', views.update_regions, name='update_regions'),
    path('delete_regions/', views.delete_regions, name='delete_regions'),
    path('forecasts/', views.forecasts, name='Forecast'),
    path('forecast_types/', views.forecast_types, name='Forecast-Type'),
    path('forecast_accuracy/', views.forecast_accuracy, name='Forecast-Accuracy'),
    path('accuracy-graph/', views.accuracy_graph_view, name='accuracy_graph'),
]
