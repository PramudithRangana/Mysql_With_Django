from django.shortcuts import render
# from django.http import HttpResponse
from .models import WeatherStations, WeatherAlerts, WeatherData, SeasonalForecasts, Regions, Forecasts, ForecastTypes, ForecastAccuracy
from django.utils.timezone import localtime


# Create your views here.
def home(request):
    context = {
        'title': 'Weather Home',
    }
    return render(request, 'weather_templates/home.html', context)


def weather_station(request):
    weather_st = WeatherStations.objects.all()
    context = {
        'title': 'Weather Station',
        'weather_st': weather_st
    }
    return render(request, 'weather_templates/weatherSt.html', context)
    # return HttpResponse('<h1>Weather Home Page</h1>')


def weather_data(request):
    weather_dt = WeatherData.objects.all()
    context = {
        'title': 'Weather Data',
        'weather_dt': weather_dt
    }
    return render(request, 'weather_templates/weatherData.html', context)


def weather_alerts(request):
    weather_alt = WeatherAlerts.objects.all()
    context = {
        'title': 'Weather Alerts',
        'weather_alt': weather_alt
    }
    return render(request, 'weather_templates/weatherAlt.html', context)


def seasonal_forecasts(request):
    seas_fore = SeasonalForecasts.objects.all()
    context = {
        'title': 'Seasonal Forecast',
        'seas_fore': seas_fore
    }
    return render(request, 'weather_templates/seasFore.html', context)


def regions(request):
    reg = Regions.objects.all()
    context = {
        'title': 'Regions',
        'reg': reg
    }
    return render(request, 'weather_templates/reg.html', context)


def forecasts(request):
    forecasting = Forecasts.objects.all()
    context = {
        'title': 'Forecasting',
        'forecasting': forecasting
    }
    return render(request, 'weather_templates/forecasting.html', context)


def forecast_types(request):
    fore_type = ForecastTypes.objects.all()
    context = {
        'title': 'Forecast Type',
        'fore_type': fore_type
    }
    return render(request, 'weather_templates/fore_type.html', context)


def forecast_accuracy(request):
    fore_acc = ForecastAccuracy.objects.all()
    context = {
        'title': 'Forecast Accuracy',
        'fore_acc': fore_acc
    }
    return render(request, 'weather_templates/fore_acc.html', context)


def accuracy_graph_view(request):
    data = ForecastAccuracy.objects.values('date_time', 'error_margin', 'accuracy_percentage')

    timestamps = [localtime(entry['date_time']).strftime('%Y-%m-%d %H:%M:%S') for entry in data]
    error_margins = [float(entry['error_margin']) if entry['error_margin'] is not None else None for entry in data]
    accuracy_percentages = [float(entry['accuracy_percentage']) if entry['accuracy_percentage'] is not None else None for entry in data]

    context = {
        'title': 'Forecast Accuracy Graph',
        'timestamps': timestamps,
        'error_margins': error_margins,
        'accuracy_percentages': accuracy_percentages,
    }
    return render(request, 'weather_templates/accuracy_graph.html', context)
