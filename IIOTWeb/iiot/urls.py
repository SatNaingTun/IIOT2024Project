from django.contrib import admin
from django.urls import include,path

# from IIOTWeb import iiot
from . import views

# from .views import iiot

urlpatterns = [
    # path("", views.index,name='iiot'),

    path("test/", views.test,name='test'),
    # path("testLocal/", views.testLocal,name='testLocal'),
    path("reg/inputs/", views.registerInputDevice,name='RegisterInput'),
    # path("mqtt/", views.mqtt_view,name='Mqtt'),
    path("", views.listDevices,name='ListDevices'),
    path("reg/mqtt/", views.registerMqtt,name='RegMqtt'),
    path("reg/influx/", views.addInfluxDB,name='RegInflux'),
    path("del/influx/<uuid:device_id>/", views.removeInfluxDB,name='RemoveInflux'),
    path("list/influx/measurement/", views.listMeasurements,name='ListMeasurement'),
    path("edit/influx/measurement/<uuid:id>/", views.editMeasurement,name='EditMeasurement'),
    path("del/influx/measurement/<uuid:id>/", views.removeMeasurement,name='RemoveMeasurement'),
    path("add/influx/measurement/", views.addInfluxMeasurement,name='AddMeasurement'),
    path("reg/influx/", views.influx_database_view,name='RegInflux'),
    path("edit/influx/<uuid:device_id>/", views.editInfluxDB,name='EditInflux'),
    
    path("edit/mqtt/<uuid:id>/", views.editMqtt,name='EditMqtt'),
    path("del/mqtt/<uuid:id>/", views.removeMqtt,name='RemoveMqtt'),
    path("edit/inputs/<uuid:device_id>/", views.editInputDevice,name='EditInput'),
    path("del/inputs/<uuid:device_id>/", views.removeInputDevice,name='RemoveInputDevice'),
    path("reg/inputs/<uuid:device_id>/address/", views.addInputAddress,name='RegInputAddress'),
    # path("reg/inputs/address/", views.addInputAddress,name='RegInputAddress2'),
    path("list/inputs/addresses/", views.listInputAddresses,name='ListInputAddress'),
    path("edit/inputs/address/<uuid:address_id>/", views.editInputAddress,name='EditAddress'),
    path("del/inputs/address/<uuid:address_id>/", views.removeInputAddress,name='RemoveInputAddress'),
    path("testrun/", views.testRun,name='TestRun'),
    path("server/info/", views.pi_profile_view,name='ServerInfo'),
    
    ]