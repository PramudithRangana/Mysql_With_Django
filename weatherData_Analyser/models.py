# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models


class AuthGroup(models.Model):
    name = models.CharField(unique=True, max_length=150)

    class Meta:
        managed = False
        db_table = 'auth_group'


class AuthGroupPermissions(models.Model):
    id = models.BigAutoField(primary_key=True)
    group = models.ForeignKey(AuthGroup, models.DO_NOTHING)
    permission = models.ForeignKey('AuthPermission', models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_group_permissions'
        unique_together = (('group', 'permission'),)


class AuthPermission(models.Model):
    name = models.CharField(max_length=255)
    content_type = models.ForeignKey('DjangoContentType', models.DO_NOTHING)
    codename = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 'auth_permission'
        unique_together = (('content_type', 'codename'),)


class AuthUser(models.Model):
    password = models.CharField(max_length=128)
    last_login = models.DateTimeField(blank=True, null=True)
    is_superuser = models.IntegerField()
    username = models.CharField(unique=True, max_length=150)
    first_name = models.CharField(max_length=150)
    last_name = models.CharField(max_length=150)
    email = models.CharField(max_length=254)
    is_staff = models.IntegerField()
    is_active = models.IntegerField()
    date_joined = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'auth_user'


class AuthUserGroups(models.Model):
    id = models.BigAutoField(primary_key=True)
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)
    group = models.ForeignKey(AuthGroup, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_user_groups'
        unique_together = (('user', 'group'),)


class AuthUserUserPermissions(models.Model):
    id = models.BigAutoField(primary_key=True)
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)
    permission = models.ForeignKey(AuthPermission, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_user_user_permissions'
        unique_together = (('user', 'permission'),)


class ClimateTrends(models.Model):
    trend_id = models.CharField(primary_key=True, max_length=12)
    station = models.ForeignKey('WeatherStations', models.DO_NOTHING, blank=True, null=True)
    parameter = models.CharField(max_length=50, blank=True, null=True)
    start_year = models.TextField(blank=True, null=True)  # This field type is a guess.
    end_year = models.TextField(blank=True, null=True)  # This field type is a guess.
    average_value = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True)
    change_rate = models.DecimalField(max_digits=5, decimal_places=3, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'climate_trends'


class DjangoAdminLog(models.Model):
    action_time = models.DateTimeField()
    object_id = models.TextField(blank=True, null=True)
    object_repr = models.CharField(max_length=200)
    action_flag = models.PositiveSmallIntegerField()
    change_message = models.TextField()
    content_type = models.ForeignKey('DjangoContentType', models.DO_NOTHING, blank=True, null=True)
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'django_admin_log'


class DjangoContentType(models.Model):
    app_label = models.CharField(max_length=100)
    model = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 'django_content_type'
        unique_together = (('app_label', 'model'),)


class DjangoMigrations(models.Model):
    id = models.BigAutoField(primary_key=True)
    app = models.CharField(max_length=255)
    name = models.CharField(max_length=255)
    applied = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'django_migrations'


class DjangoSession(models.Model):
    session_key = models.CharField(primary_key=True, max_length=40)
    session_data = models.TextField()
    expire_date = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'django_session'


class ForecastAccuracy(models.Model):
    accuracy_id = models.CharField(primary_key=True, max_length=12)
    forecast = models.ForeignKey('Forecasts', models.DO_NOTHING, blank=True, null=True)
    error_margin = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True)
    accuracy_percentage = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True)
    date_time = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'forecast_accuracy'


class ForecastTypes(models.Model):
    type_id = models.CharField(primary_key=True, max_length=10)
    type_name = models.CharField(max_length=40)
    type_description = models.CharField(max_length=100, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'forecast_types'


class Forecasts(models.Model):
    forecast_id = models.CharField(primary_key=True, max_length=12)
    station = models.ForeignKey('WeatherStations', models.DO_NOTHING, blank=True, null=True)
    forecast_year = models.TextField(blank=True, null=True)  # This field type is a guess.
    type = models.ForeignKey(ForecastTypes, models.DO_NOTHING, blank=True, null=True)
    forecast_value = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True)
    forecast_date = models.DateField(blank=True, null=True)
    actual_value = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'forecasts'


class ProvincialNames(models.Model):
    prov_id = models.AutoField(primary_key=True)
    province_name = models.CharField(max_length=30, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'provincial_names'


class Regions(models.Model):
    region_id = models.CharField(primary_key=True, max_length=15)
    region_name = models.CharField(max_length=30, blank=True, null=True)
    province = models.CharField(max_length=25, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'regions'


class SeasonalForecasts(models.Model):
    season_id = models.CharField(primary_key=True, max_length=12)
    station = models.ForeignKey('WeatherStations', models.DO_NOTHING, blank=True, null=True)
    forecast_year = models.TextField(blank=True, null=True)  # This field type is a guess.
    season = models.CharField(max_length=50, blank=True, null=True)
    forecast_value = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True)
    forecast_type = models.ForeignKey(ForecastTypes, models.DO_NOTHING, blank=True, null=True)
    forecast_date = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'seasonal_forecasts'


class WeatherAlerts(models.Model):
    alert_id = models.CharField(primary_key=True, max_length=12)
    station = models.ForeignKey('WeatherStations', models.DO_NOTHING, blank=True, null=True)
    alert_type = models.CharField(max_length=100, blank=True, null=True)
    alert_description = models.TextField(blank=True, null=True)
    issued_date = models.DateTimeField(blank=True, null=True)
    severity = models.CharField(max_length=8, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'weather_alerts'


class WeatherData(models.Model):
    weatherdata_id = models.CharField(db_column='weatherData_id', max_length=15, blank=True, null=True)  # Field name made lowercase.
    station = models.ForeignKey('WeatherStations', models.DO_NOTHING, blank=True, null=True)
    observation_date = models.DateField(blank=True, null=True)
    temperature = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True)
    rainfall = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True)
    wind_speed = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True)
    humidity = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True)
    observation_time = models.TimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'weather_data'


class WeatherStations(models.Model):
    station_id = models.CharField(primary_key=True, max_length=12)  # The composite primary key (station_id, station_name) found, that is not supported. The first column is selected.
    station_name = models.CharField(max_length=15)
    st_location = models.CharField(max_length=25, blank=True, null=True)
    latitude = models.DecimalField(max_digits=9, decimal_places=6, blank=True, null=True)
    longitude = models.DecimalField(max_digits=9, decimal_places=6, blank=True, null=True)
    region = models.ForeignKey(Regions, models.DO_NOTHING, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'weather_stations'
        unique_together = (('station_id', 'station_name'),)
