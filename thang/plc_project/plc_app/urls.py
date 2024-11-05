# plc_app/urls.py
from django.urls import path
from .views import plc_view, create_database_view

urlpatterns = [
    path('', plc_view, name='plc_view'),
    path('create_database/', create_database_view, name='create_database_view'),
]