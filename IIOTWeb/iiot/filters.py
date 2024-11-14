# filters
import django_filters

from .models import InputAddresses,InfluxMeasurement

class InputAddressFilter(django_filters.FilterSet):
    class Meta:
        model=InputAddresses
        fields={'device':['exact']}
        # db_table=''
        # managed=True
        # verbose_name='ModelName'
        # verbose_name_plural='ModelNames'


class InfluxMeasurementFilter(django_filters.FilterSet):
    class Meta:
        model=InfluxMeasurement
        fields={'data':['exact'],'database':['exact']}