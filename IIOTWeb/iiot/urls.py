from django.contrib import admin
from django.urls import include,path

# from IIOTWeb import iiot
from . import views

# from .views import iiot

urlpatterns = [
    # path("", views.index,name='iiot'),
    path("", views.test,name='test'),
    path("test/", views.test,name='test'),
    path("list/", views.list_view,name='list'),
    ]