from django.db import models
from django.utils.timezone import localtime


# Create your models here.
class ForecastAccuracy(models.Model):
    accuracy_id = models.CharField(primary_key=True, max_length=12)
    forecast = models.ForeignKey('Forecasts', models.DO_NOTHING, blank=True, null=True)
    error_margin = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True)
    accuracy_percentage = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True)
    date_time = models.DateTimeField()

    objects = models.Manager()  # Explicitly add a manager

    class Meta:
        managed = False
        db_table = 'forecast_accuracy'

    def __str__(self):
        return self.accuracy_id

    def formatted_date_time(self):
        """
        Returns the issued_date in the format 'YYYY Month DD, Day HH:MM:SS'.
        """
        if self.date_time:
            local_time = localtime(self.date_time)  # Adjust to local timezone if needed
            return local_time.strftime('%Y %B %d, %A %H:%M:%S')
        return None


class ForecastTypes(models.Model):
    type_id = models.CharField(primary_key=True, max_length=10)
    type_name = models.CharField(max_length=40)
    type_description = models.CharField(max_length=100, blank=True, null=True)

    objects = models.Manager()  # Explicitly add a manager

    class Meta:
        managed = False
        db_table = 'forecast_types'

    def __str__(self):
        return self.type_id


class Forecasts(models.Model):
    forecast_id = models.CharField(primary_key=True, max_length=12)
    station = models.ForeignKey('WeatherStations', models.DO_NOTHING, blank=True, null=True)
    forecast_year = models.TextField(blank=True, null=True)  # This field type is a guess.
    type = models.ForeignKey(ForecastTypes, models.DO_NOTHING, blank=True, null=True)
    forecast_value = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True)
    forecast_date = models.DateField(blank=True, null=True)
    actual_value = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True)

    objects = models.Manager()  # Explicitly add a manager

    class Meta:
        managed = False
        db_table = 'forecasts'

    def __str__(self):
        return self.forecast_id

    def formatted_forecast_date(self):
        """
        Returns the observation_date in the format 'YYYY Month DD, Day'.
        """
        if self.forecast_date:
            return self.forecast_date.strftime('%Y %B %d, %A')
        print("Debug: observation_date is None or invalid")
        return None


class ProvincialNames(models.Model):
    prov_id = models.AutoField(primary_key=True)
    province_name = models.CharField(max_length=30, blank=True, null=True)

    objects = models.Manager()  # Explicitly add a manager

    class Meta:
        managed = False
        db_table = 'provincial_names'

    def __str__(self):
        return self.prov_id


class Regions(models.Model):
    region_id = models.CharField(primary_key=True, max_length=15)
    region_name = models.CharField(max_length=30, blank=True, null=True)
    province = models.CharField(max_length=25, blank=True, null=True)

    objects = models.Manager()  # Explicitly add a manager

    class Meta:
        managed = False
        db_table = 'regions'

    def __str__(self):
        return self.region_id


class SeasonalForecasts(models.Model):
    season_id = models.CharField(primary_key=True, max_length=12)
    station = models.ForeignKey('WeatherStations', models.DO_NOTHING, blank=True, null=True)
    forecast_year = models.TextField(blank=True, null=True)  # This field type is a guess.
    season = models.CharField(max_length=50, blank=True, null=True)
    forecast_value = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True)
    forecast_type = models.ForeignKey(ForecastTypes, models.DO_NOTHING, blank=True, null=True)
    forecast_date = models.DateTimeField(blank=True, null=True)

    objects = models.Manager()  # Explicitly add a manager

    class Meta:
        managed = False
        db_table = 'seasonal_forecasts'

    def __str__(self):
        return self.season_id

    def formatted_forecast_date(self):
        """
        Returns the issued_date in the format 'YYYY Month DD, Day HH:MM:SS'.
        """
        if self.forecast_date:
            local_time = localtime(self.forecast_date)  # Adjust to local timezone if needed
            return local_time.strftime('%Y %B %d, %A %H:%M:%S')
        return None


class WeatherAlerts(models.Model):
    alert_id = models.CharField(primary_key=True, max_length=12)
    station = models.ForeignKey('WeatherStations', models.DO_NOTHING, blank=True, null=True)
    alert_type = models.CharField(max_length=100, blank=True, null=True)
    alert_description = models.TextField(blank=True, null=True)
    issued_date = models.DateTimeField(blank=True, null=True)
    severity = models.CharField(max_length=8, blank=True, null=True)

    objects = models.Manager()  # Explicitly add a manager

    class Meta:
        managed = False
        db_table = 'weather_alerts'

    def __str__(self):
        return self.alert_id

    def formatted_issued_date(self):
        """
        Returns the issued_date in the format 'YYYY Month DD, Day HH:MM:SS'.
        """
        if self.issued_date:
            local_time = localtime(self.issued_date)  # Adjust to local timezone if needed
            return local_time.strftime('%Y %B %d, %A %H:%M:%S')
        return None


class WeatherData(models.Model):
    weatherdata_id = models.CharField(primary_key=True, max_length=15)  # Field name made lowercase.
    station = models.ForeignKey('WeatherStations', models.DO_NOTHING, blank=True, null=True)
    observation_date = models.DateField(blank=True, null=True)
    temperature = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True)
    rainfall = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True)
    wind_speed = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True)
    humidity = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True)
    observation_time = models.TimeField(blank=True, null=True)

    objects = models.Manager()  # Explicitly add a manager

    class Meta:
        managed = False
        db_table = 'weather_data'

    def __str__(self):
        return self.weatherdata_id

    def formatted_observation_date(self):
        """
        Returns the observation_date in the format 'YYYY Month DD, Day'.
        """
        if self.observation_date:
            return self.observation_date.strftime('%Y %B %d, %A')
        print("Debug: observation_date is None or invalid")
        return None


class WeatherStations(models.Model):
    station_id = models.CharField(primary_key=True, max_length=12)  # The composite primary key (station_id, station_name) found, that is not supported. The first column is selected.
    station_name = models.CharField(max_length=15)
    st_location = models.CharField(max_length=25, blank=True, null=True)
    latitude = models.DecimalField(max_digits=9, decimal_places=6, blank=True, null=True)
    longitude = models.DecimalField(max_digits=9, decimal_places=6, blank=True, null=True)
    region = models.ForeignKey(Regions, models.DO_NOTHING, blank=True, null=True)

    objects = models.Manager()  # Explicitly add a manager

    class Meta:
        managed = False
        db_table = 'weather_stations'
        unique_together = (('station_id', 'station_name'),)

    def __str__(self):
        return self.station_id
