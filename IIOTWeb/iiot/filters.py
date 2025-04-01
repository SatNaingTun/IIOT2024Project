# filters
import django_filters

from .models import InputAddresses, InfluxMeasurement


class InputAddressFilter(django_filters.FilterSet):
    class Meta:
        model = InputAddresses
        fields = {'device': ['exact']}


class InfluxMeasurementFilter(django_filters.FilterSet):
    class Meta:
        model = InfluxMeasurement
        fields = {'data': ['exact'], 'database': ['exact']}
