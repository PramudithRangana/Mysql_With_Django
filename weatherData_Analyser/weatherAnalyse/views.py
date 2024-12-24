from django.shortcuts import render, get_object_or_404
from .models import WeatherStations, WeatherAlerts, WeatherData, SeasonalForecasts, Regions, Forecasts, ForecastTypes, \
    ForecastAccuracy
from django.utils.timezone import localtime

from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json


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


def weather_data(request):
    weather_dt = WeatherData.objects.all()
    context = {
        'title': 'Weather Data',
        'weather_dt': weather_dt
    }
    return render(request, 'weather_templates/weatherData.html', context)


def get_new_alert_id(request):
    try:
        # Use the custom manager to call the stored procedure
        new_alert_id = WeatherAlerts.objects.generate_new_alert_id()

        if new_alert_id:
            return JsonResponse({"new_alert_id": new_alert_id})
        else:
            return JsonResponse({"error": "Failed to generate Alert ID"}, status=500)

    except Exception as e:
        print(f"Error: {e}")
        return JsonResponse({"error": "Something went wrong"}, status=500)


def weather_alerts(request):
    weather_alt = WeatherAlerts.objects.all()
    weather_stations = WeatherStations.objects.all()  # Fetch all stations

    return render(request, 'weather_templates/weatherAlt.html', {
        'title': 'Weather Alerts',
        'weather_alt': weather_alt,
        'weather_stations': weather_stations
    })


@csrf_exempt
def add_weather_alert(request):
    if request.method == 'POST':
        import json
        data = json.loads(request.body)

        # Process each alert in the data
        for alert in data:
            alert_id = alert.get('alert_id')
            station_id = alert.get('station_id')
            alert_type = alert.get('alert_type')
            alert_description = alert.get('alert_description')
            issued_date = alert.get('issued_date')
            severity = alert.get('severity')

            # Create new record in the database
            WeatherAlerts.objects.create(
                alert_id=alert_id,
                station_id=station_id,
                alert_type=alert_type,
                alert_description=alert_description,
                issued_date=issued_date,
                severity=severity
            )

        return JsonResponse({"message": "Alert added successfully."}, status=201)

    return JsonResponse({"error": "Invalid request method."}, status=400)


@csrf_exempt
def save_all_weather_alerts(request):
    if request.method == 'POST':
        import json
        updates = json.loads(request.body)

        # Debug incoming data
        print("Received updates:", updates)

        # Iterate through all updates and save them
        for update in updates:
            alert_id = update.get('alert_id')
            station_id = update.get('station_id')
            alert_type = update.get('alert_type')
            alert_description = update.get('alert_description')
            issued_date = update.get('issued_date')
            severity = update.get('severity')

            # Update or create the alert
            obj, created = WeatherAlerts.objects.update_or_create(
                alert_id=alert_id,
                defaults={
                    'station_id': station_id,
                    'alert_type': alert_type,
                    'alert_description': alert_description,
                    'issued_date': issued_date,
                    'severity': severity
                }
            )
            # Print for debugging
            print(f"Alert ID {alert_id}: {'Created' if created else 'Updated'}.")

        return JsonResponse({"message": "All alerts saved successfully."}, status=200)

    return JsonResponse({"error": "Invalid request method."}, status=400)


@csrf_exempt
def update_weather_alerts(request):
    if request.method == 'POST':
        import json
        print("POST request received")
        try:
            updates = json.loads(request.body)
            print("Updates:", updates)
        except json.JSONDecodeError as e:
            print("JSON decode error:", e)
            return JsonResponse({"error": "Invalid JSON payload"}, status=400)

        for update in updates:
            print("Processing update:", update)
            alert_id = update.get('alert_id')
            station_id = update.get('station_id')
            alert_type = update.get('alert_type')
            alert_description = update.get('alert_description')
            issued_date = update.get('issued_date')
            severity = update.get('severity')

            # Debug individual fields
            print(f""" 
                Alert ID: {alert_id}
                Station ID: {station_id}
                Alert Type: {alert_type}
                Description: {alert_description}
                Issued Date: {issued_date}
                Severity: {severity}
             """)

            affected_rows = WeatherAlerts.objects.filter(alert_id=alert_id).update(
                station_id=station_id,
                alert_type=alert_type,
                alert_description=alert_description,
                issued_date=issued_date,
                severity=severity,
            )

            print(f"Alert ID {alert_id}: {affected_rows} row(s) updated.")

        return JsonResponse({"message": "Updates processed."}, status=200)
    return JsonResponse({"error": "Invalid request method."}, status=400)


@csrf_exempt
def delete_weather_alerts(request):
    if request.method == 'POST':
        import json
        alert_ids = json.loads(request.body)  # Expecting a list of alert_ids

        # Debug incoming data
        print("Received alert IDs to delete:", alert_ids)

        # Deleting the alerts by alert_id
        deleted_count, _ = WeatherAlerts.objects.filter(alert_id__in=alert_ids).delete()

        print(f"Deleted {deleted_count} weather alert(s).")

        return JsonResponse({"message": f"{deleted_count} alert(s) deleted."}, status=200)

    return JsonResponse({"error": "Invalid request method."}, status=400)


def seasonal_forecasts(request):
    seas_fore = SeasonalForecasts.objects.all()
    context = {
        'title': 'Seasonal Forecast',
        'seas_fore': seas_fore
    }
    return render(request, 'weather_templates/seasFore.html', context)


def get_new_region_id(request):
    if request.method == "GET":
        try:
            # Extract region_name and province from the query parameters
            region_name = request.GET.get('region_name', '').strip()
            province = request.GET.get('province', '').strip()

            if not region_name or not province:
                return JsonResponse({"error": "Both region_name and province are required."}, status=400)

            # Generate new region_id
            new_region_id = Regions.generate_region_id(region_name, province)

            return JsonResponse({"new_region_id": new_region_id}, status=200)
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=400)
    else:
        return JsonResponse({"error": "Invalid request method"}, status=405)


def regions(request):
    reg = Regions.objects.all()
    context = {
        'title': 'Regions',
        'reg': reg
    }
    return render(request, 'weather_templates/reg.html', context)


def save_all_regions(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            _regions = data.get('regions', [])

            for region in _regions:
                region_id = region.get('region_id')
                region_name = region.get('region_name')
                province = region.get('province')

                if not region_id:  # If `region_id` is empty, generate a new one
                    region_id = Regions.generate_region_id(region_name, province)

                # Update or create region records
                if region_id:
                    Regions.objects.update_or_create(
                        region_id=region_id,
                        defaults={'region_name': region_name, 'province': province}
                    )

            return JsonResponse({"message": "Regions saved successfully!"}, status=200)
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=400)
    else:
        return JsonResponse({"error": "Invalid request method"}, status=405)


@csrf_exempt
def update_regions(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body).get("data", [])
            for item in data:
                region_id = item.get("region_id")
                region_name = item.get("region_name")
                province = item.get("province")

                # Update the record
                region = Regions.objects.get(region_id=region_id)
                region.region_name = region_name
                region.province = province
                region.save()

            return JsonResponse({"message": "Selected rows updated successfully!"}, status=200)
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=400)
    return JsonResponse({"error": "Invalid request method"}, status=405)


@csrf_exempt
def delete_regions(request):
    if request.method == "POST":
        ids = json.loads(request.body).get("data", [])
        Regions.objects.filter(region_id__in=ids).delete()
        return JsonResponse({"message": "Selected rows deleted successfully!"})


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
    accuracy_percentages = [float(entry['accuracy_percentage']) if entry['accuracy_percentage'] is not None else None
                            for entry in data]

    context = {
        'title': 'Forecast Accuracy Graph',
        'timestamps': timestamps,
        'error_margins': error_margins,
        'accuracy_percentages': accuracy_percentages,
    }
    return render(request, 'weather_templates/accuracy_graph.html', context)
