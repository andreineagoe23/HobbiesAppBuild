from django.conf import settings
from django.contrib import admin
from django.urls import include, path
from django.http import HttpResponse

from .views import main_spa

urlpatterns = [
    path('', main_spa),
]
