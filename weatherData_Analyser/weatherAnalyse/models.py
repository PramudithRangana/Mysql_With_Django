from django.db import models, connection
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

    @classmethod
    def generate_forecast_id(cls, init_symbol="FT"):
        """
        Generate a new region_id using the `fc_id_gen` stored procedure.
        """
        try:
            with connection.cursor() as cursor:
                cursor.callproc('fc_id_gen', [init_symbol])
                result = cursor.fetchone()
                return result[0] if result else None
        except Exception as e:
            raise RuntimeError(f"Error generating Forecast ID: {str(e)}")


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

    @classmethod
    def generate_region_id(cls, region_name, province):
        """
        Generate a new region_id dynamically based on region_name and province.
        """
        try:
            # Create initials for region_name and province
            region_initials = ''.join(word[0] for word in region_name.split()).lower()
            province_initials = ''.join(word[0] for word in province.split()).lower()

            # Call the stored procedure with province initials
            with connection.cursor() as cursor:
                cursor.callproc('reg_id_gen', [province_initials])
                result = cursor.fetchone()
                sequence_number = result[0] if result else '0001'

            # Construct the new region_id
            return f"{region_initials}/{province_initials} - {sequence_number}"
        except Exception as e:
            raise RuntimeError(f"Error generating region_id: {str(e)}")


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


# Define the custom manager
class WeatherAlertManager(models.Manager):
    @staticmethod
    def generate_new_alert_id():
        """Call the stored procedure to generate a new alert_id"""
        try:
            with connection.cursor() as cursor:
                # Call the stored procedure
                cursor.callproc('wa_id_gen')  # Name of the stored procedure

                # Fetch the result from the stored procedure
                new_alert_id = cursor.fetchone()[0]
            return new_alert_id

        except Exception as e:
            print(f"Error generating new Alert ID: {e}")
            return None


# Define the model
class WeatherAlerts(models.Model):
    alert_id = models.CharField(primary_key=True, max_length=12)
    station = models.ForeignKey('WeatherStations', models.DO_NOTHING, blank=True, null=True)
    alert_type = models.CharField(max_length=100, blank=True, null=True)
    alert_description = models.TextField(blank=True, null=True)
    issued_date = models.DateTimeField(blank=True, null=True)
    severity = models.CharField(max_length=8, blank=True, null=True)

    objects = WeatherAlertManager()  # Assign the custom manager here

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
    station_id = models.CharField(primary_key=True,
                                  max_length=12)  # The composite primary key (station_id, station_name) found, that is not supported. The first column is selected.
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
