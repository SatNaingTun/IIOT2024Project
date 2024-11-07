from django.contrib import admin
from django.urls import include,path

# from IIOTWeb import iiot
from . import views

# from .views import iiot

urlpatterns = [
    # path("", views.index,name='iiot'),

    path("test/", views.test,name='test'),
    path("testLocal/", views.testLocal,name='testLocal'),
    path("reg/inputs/", views.registerInputDevice,name='RegisterInput'),
    path("mqtt/", views.mqtt_view,name='Mqtt'),
    path("", views.listDevices,name='ListDevices'),
    path("reg/mqtt/", views.registerMqtt,name='RegMqtt'),
    path("edit/mqtt/<uuid:id>/", views.editMqtt,name='EditMqtt'),
    path("edit/inputs/<uuid:device_id>/", views.editInputDevice,name='EditInput'),
    path("reg/inputs/<uuid:device_id>/address/", views.addInputAddress,name='AddInputAddress'),
    path("list/inputs/addresses/", views.listInputAddresses,name='ListInputAddress'),
    path("edit/inputs/address/<uuid:address_id>/", views.editInputAddress,name='EditAddress')
    
    ]