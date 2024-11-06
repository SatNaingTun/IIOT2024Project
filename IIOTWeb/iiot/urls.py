from django.contrib import admin
from django.urls import include,path

# from IIOTWeb import iiot
from . import views

# from .views import iiot

urlpatterns = [
    # path("", views.index,name='iiot'),
    path("", views.test,name='test'),
    path("testLocal/", views.testLocal,name='testLocal'),
    path("reg/inputs/", views.registerInputDevice,name='RegisterInput'),
    path("mqtt/", views.mqtt_view,name='Mqtt'),
    path("list/inputs/", views.listInputDevices,name='ListInput'),
    path("reg/mqtt/", views.listInputDevices,name='RegMqtt'),
    path("edit/inputs/<str:id>/", views.editInputDevice,name='EditInput'),
    ]