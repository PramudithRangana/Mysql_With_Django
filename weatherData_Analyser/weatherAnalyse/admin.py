from django.contrib import admin
from .models import WeatherStations, WeatherData, WeatherAlerts, SeasonalForecasts, Regions, Forecasts, ForecastTypes, ForecastAccuracy


# Register your models here.
# Register Weather_Station
class WeatherST_tbl(admin.ModelAdmin):
    list_display = ['station_id', 'station_name', 'st_location', 'latitude', 'longitude', 'region_id']


admin.site.register(WeatherStations, WeatherST_tbl)


# Register WeatherData
class WeatherData_tbl(admin.ModelAdmin):
    list_display = ['weatherdata_id', 'station', 'observation_date', 'temperature', 'rainfall', 'wind_speed',
                    'humidity', 'observation_time']


admin.site.register(WeatherData, WeatherData_tbl)


class WeatherAlt_tbl(admin.ModelAdmin):
    list_display = ['alert_id', 'station', 'alert_type', 'alert_description', 'issued_date', 'severity']


admin.site.register(WeatherAlerts, WeatherAlt_tbl)


class WeatherSf_tbl(admin.ModelAdmin):
    list_display = ['season_id', 'station', 'forecast_year', 'season', 'forecast_value', 'forecast_type',
                    'forecast_date']


admin.site.register(SeasonalForecasts, WeatherSf_tbl)


class WeatherRg_tbl(admin.ModelAdmin):
    list_display = ['region_id', 'region_name', 'province']


admin.site.register(Regions, WeatherRg_tbl)


class WeatherFc_tbl(admin.ModelAdmin):
    list_display = ['forecast_id', 'station', 'forecast_year', 'type', 'forecast_value', 'forecast_date',
                    'actual_value']


admin.site.register(Forecasts, WeatherFc_tbl)


class WeatherFt_tbl(admin.ModelAdmin):
    list_display = ['type_id', 'type_name', 'type_description']


admin.site.register(ForecastTypes, WeatherFt_tbl)


class WeatherFa_tbl(admin.ModelAdmin):
    list_display = ['accuracy_id', 'forecast', 'error_margin', 'accuracy_percentage', 'date_time']


admin.site.register(ForecastAccuracy, WeatherFa_tbl)
