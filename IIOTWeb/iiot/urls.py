from django.contrib import admin
from django.urls import include,path

# from IIOTWeb import iiot
from . import views

# from .views import iiot

urlpatterns = [
    # path("", views.index,name='iiot'),
    path("", views.test,name='test'),
    path("testLocal/", views.testLocal,name='testLocal'),
    path("regInputDev/", views.registerInputDevice,name='RegisterInput'),
    path("mqtt/", views.mqtt_view,name='Mqtt'),
    path("listInputDev/", views.listInputDevices,name='ListInput'),
    ]