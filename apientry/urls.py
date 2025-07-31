from django.urls import path
from .api import app_v01

urlpatterns = [
    path("v1/", app_v01.urls, name='ams'),
]